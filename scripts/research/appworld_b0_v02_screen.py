"""Freeze a public-data-only AppWorld Clean screen manifest."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANDATORY = ["6c2c621_1", "530b157_1", "6171bbc_1"]
EXTRAS = ["50e1ac9_1", "0d8a4ee_1"]
FAMILY_APPS = {
    "6c2c621": ["simple_note", "file_system"],
    "530b157": ["phone", "venmo"],
    "6171bbc": ["spotify"],
    "50e1ac9": ["spotify"],
    "0d8a4ee": ["phone", "venmo"],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/appworld_b0_v02/clean_screen_manifest.json")
    parser.add_argument("--report", default="docs/research/APPWORLD_CLEAN_SCREEN_V02.md")
    args = parser.parse_args()
    dev_ids = [x.strip() for x in (ROOT / "data/datasets/dev.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
    chosen = [x for x in MANDATORY + EXTRAS if x in dev_ids]
    cases = []
    for task_id in chosen:
        spec = json.loads((ROOT / "data/tasks" / task_id / "specs.json").read_text(encoding="utf-8"))
        family = task_id.split("_", 1)[0]
        cases.append({
            "task_id": task_id,
            "apps": FAMILY_APPS.get(family, []),
            "public_instruction": str(spec.get("instruction", "")),
            "screen_status": "FROZEN",
            "selection_reason": "mandatory case" if task_id in MANDATORY else "public dev candidate with a distinct or complementary tool family",
        })
    excluded = []
    for task_id in dev_ids:
        if task_id not in chosen:
            excluded.append({"task_id": task_id, "reason": "held out to keep the paid screen at five cases; no hidden-score inspection"})
    manifest = {
        "status": "FROZEN", "schema_version": "appworld_b0_v02_clean_screen_1",
        "created_utc": datetime.now(UTC).isoformat(), "split": "dev",
        "model": "deepseek-flash", "temperature": 0.0, "thinking": "disabled",
        "seed": 42, "max_tool_iterations": 12, "long_horizon_max_stages": 3,
        "parallel_plan": {"initial": 2, "after_isolation_check": 4},
        "approved_cap_usd": 4.0, "tools": "official AppWorld public function-calling API only",
        "frozen_cases": cases, "excluded_or_held_out": excluded,
        "ground_truth_used": False, "official_scoring": "world.evaluate() after execution only",
    }
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# AppWorld Clean Screen v02", "", "状态：已冻结（只使用公开 dev split 和公开任务说明）。", "", "## 冻结 Case", ""]
    for case in cases:
        lines += [f"- `{case['task_id']}`（{', '.join(case['apps'])}）：{case['public_instruction']}"]
    lines += ["", "## 协议", "", "- 模型：`deepseek-flash`，温度 0，关闭 Thinking，Seed 42。", "- 每条 Episode 最多 3 个长程阶段，每阶段最多 12 次工具循环。", "- 正式运行最多 5 个 Case × 2 个 arm；先并行 2 条，隔离检查通过后才提高到 4 条。", "- 费用上限 4 美元；官方评分只在 Episode 结束后调用 `world.evaluate()`。", "- 所有未入选的公开 dev Case 和筛选原因保存在 manifest，不用隐藏答案筛选。", ""]
    (ROOT / args.report).write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": "FROZEN", "frozen_cases": chosen, "excluded_count": len(excluded)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
