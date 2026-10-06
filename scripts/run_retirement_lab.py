"""Run the paired node-retirement microcases with the configured DeepSeek API.

The result file contains fictional case prompts, model responses, and aggregate
usage. It never stores the API key or the contents of the env file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from dotenv import load_dotenv

from MAS.config import OpenRouterConfig
from MAS.llm import OpenRouterLLMClient
from MAS.self_evolved.retirement_lab import CASES, RetirementLab

SOURCE_FILES = (
    "MAS/config.py",
    "MAS/llm.py",
    "MAS/self_evolved/retirement.py",
    "MAS/self_evolved/retirement_lab.py",
    "scripts/run_retirement_lab.py",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cases", default=",".join(case.case_id for case in CASES))
    parser.add_argument("--arms", default="keep,direct,policy,guard")
    parser.add_argument("--max-calls", type=int, default=60)
    args = parser.parse_args()

    if not args.env_file.is_file():
        raise FileNotFoundError(args.env_file)
    load_dotenv(args.env_file, override=False)
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is absent; no mock experiment is permitted")
    os.environ["MAS_REQUIRE_LIVE_LLM"] = "1"
    os.environ["DEEPSEEK_THINKING"] = "disabled"
    os.environ["DEEPSEEK_MAX_TOKENS"] = "256"
    client = OpenRouterLLMClient(
        OpenRouterConfig(api_key=api_key, base_url="https://api.deepseek.com", timeout_s=120),
        {"default": "deepseek-flash", "general": "deepseek-flash"},
    )
    selected = {name.strip() for name in args.cases.split(",") if name.strip()}
    arms = tuple(name.strip() for name in args.arms.split(",") if name.strip())
    cases = [case for case in CASES if case.case_id in selected]
    if len(cases) != len(selected):
        raise ValueError(f"unknown cases: {sorted(selected - {case.case_id for case in cases})}")
    if len(set(arms)) != len(arms) or not arms:
        raise ValueError("arms must be nonempty and unique")
    lab = RetirementLab(client, max_calls=args.max_calls)
    result = {
        "schema_version": 1,
        "case_protocol_version": 3,
        "started_at_utc": datetime.now(UTC).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "source_sha256": {
            path: hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in SOURCE_FILES
        },
        "provider": "deepseek",
        "model_requested": "deepseek-flash",
        "thinking": "disabled",
        "max_output_tokens_per_call": 256,
        "max_calls": args.max_calls,
        "arms": list(arms),
        "cases": [],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for case in cases:
        result["cases"].append(lab.run_case(case, arms))
        result["calls_completed"] = lab.calls
        result["updated_at_utc"] = datetime.now(UTC).isoformat()
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(args.output)
        print(f"{case.case_id}: {lab.calls} API calls completed", flush=True)


if __name__ == "__main__":
    main()
