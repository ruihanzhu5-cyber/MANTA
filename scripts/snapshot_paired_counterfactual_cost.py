"""Freeze Pilot 08 usage, including captures without a legal native proposal."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT.parent / "manta_three_pilots_budget.json"
OUT = ROOT / "results/pilot08_counterfactual/cost_ledger_snapshot.json"


def main() -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    episodes = [row for row in ledger.get("episodes", []) if row.get("pilot") == "pilot08"]
    invalid = [row for row in ledger.get("invalid_attempts", [])
               if row.get("pilot") == "pilot08"]
    if any(row.get("pilot") == "pilot08" for row in ledger.get("inflight", [])):
        raise RuntimeError("Pilot 08 still has an inflight episode")
    upper = sum(float(row.get("cost_upper_usd", 0)) for row in episodes + invalid)
    upper += sum(float(row.get("unknown_usage_reserve_usd", 0)) for row in invalid)
    payload = {
        "snapshot_utc": datetime.now(UTC).isoformat(),
        "pilot": "pilot08", "shared_cap_usd": ledger["cap_usd"],
        "price_rule": "uncached peak input $0.30/M output $1.20/M",
        "episode_count": len(episodes), "invalid_attempt_count": len(invalid),
        "episode_token_in": sum(row.get("token_in", 0) for row in episodes),
        "episode_token_out": sum(row.get("token_out", 0) for row in episodes),
        "pilot_upper_cost_usd_including_invalid": round(upper, 7),
        "episodes": episodes, "invalid_attempts": invalid,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Pilot 08 snapshot: {len(episodes)} episodes, {len(invalid)} invalid, ${upper:.4f}")


if __name__ == "__main__":
    main()
