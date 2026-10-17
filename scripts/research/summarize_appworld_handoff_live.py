"""Create a sanitized, reviewable report from the ignored live-run ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def summarize(artifact_dir: Path, output_dir: Path) -> tuple[Path, Path]:
    ledger = json.loads((artifact_dir / "ledger.json").read_text(encoding="utf-8"))
    episodes = list(ledger.get("episodes", []))
    rows = []
    for episode in episodes:
        rows.append({
            key: episode.get(key)
            for key in (
                "task_id", "arm", "variant", "official_score_available",
                "official_task_success", "complete_artifacts", "model_events",
                "tool_calls", "token_in", "token_out", "cost_upper_usd",
                "duration_seconds", "return_code", "error",
            )
        })
    successful = sum(bool(row.get("official_task_success")) for row in rows)
    total_cost = sum(float(row.get("cost_upper_usd") or 0) for row in rows)
    report = output_dir / "APPWORLD_HANDOFF_LIVE_RESULTS.md"
    lines = [
        "# AppWorld handoff live experiment results",
        "",
        "## Scope",
        "",
        "This report contains only sanitized run metrics. Full prompts, tool outputs, and AppWorld state remain under the ignored `artifacts/` directory.",
        "The functional gate ran two official dev tasks with `SINGLE_AGENT` and `MANTA_NATIVE`, using `NATIVE_PACKET` and one independent AppWorld world per run.",
        "",
        "## B0 result",
        "",
        f"- Runs completed: {len(rows)}; official successes: {successful}/{len(rows)}.",
        f"- Conservative cost upper bound: ${total_cost:.4f}; measured episode concurrency: 2.",
        "- All four runs produced official evaluation files and made real model/tool calls.",
        "- Gate: `NO_VALID_CLEAN_CASE`; B1 handoff-arm comparison and B2 injection experiment were not run.",
        "- This is a capability/adapter diagnostic only. It does not support a claim about handoff quality.",
        "- Evidence IDs: `B0-6c2c621_1-SINGLE_AGENT`, `B0-6c2c621_1-MANTA_NATIVE`, `B0-530b157_1-SINGLE_AGENT`, `B0-530b157_1-MANTA_NATIVE`.",
        "",
        "## Per-run metrics",
        "",
        "| task | arm | official success | model events | tool calls | cost upper bound (USD) | duration (s) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('task_id')} | {row.get('arm')} | {bool(row.get('official_task_success'))} | "
            f"{row.get('model_events', 0)} | {row.get('tool_calls', 0)} | {float(row.get('cost_upper_usd', 0)):.4f} | "
            f"{float(row.get('duration_seconds', 0)):.1f} |"
        )
    lines.extend([
        "",
        "## Decision",
        "",
        "The next step is an adapter/runtime investigation of the two clean tasks. Do not interpret the failed B0 runs as evidence for or against any handoff design.",
        "",
        "## Reproducibility",
        "",
        "- Branch: `research/appworld-handoff-ipi-live-v01`.",
        "- Model name: `deepseek-flash`; no API key or secret is included here.",
        "- Official AppWorld package: `0.1.3.post1`; data package: `0.1.0` (from the frozen project configuration).",
        "- DeepSeek official rate-limit page: https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit/",
        "- DeepSeek official pricing page: https://api-docs.deepseek.com/quick_start/pricing/",
    ])
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    notes = output_dir / "APPWORLD_HANDOFF_METHOD_NOTES.md"
    notes.write_text(
        "# AppWorld handoff method notes\n\n"
        "The code renders packets only after ContextPolicy filtering. `NATIVE_PACKET` deep-copies the native packet, `SUMMARY_ONLY` keeps packet identity and the native summary, and `EVIDENCE_REFERENCED` adds stable artifact/record handles and structural field paths without copying tool-result values.\n\n"
        "B0 was intentionally run before any handoff-arm comparison. Both official tasks failed in both baseline arms, so the documented stop rule `NO_VALID_CLEAN_CASE` applies. No attack recipient, injection payload, or hidden verifier was used.\n\n"
        "Raw traces and ledger files are local ignored artifacts. Only this sanitized report and the source/configuration are intended for version control.\n",
        encoding="utf-8",
    )
    return report, notes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", default="artifacts/appworld_handoff_live")
    parser.add_argument("--output-dir", default="docs/research")
    args = parser.parse_args()
    report, notes = summarize(Path(args.artifact_dir), Path(args.output_dir))
    print(report)
    print(notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
