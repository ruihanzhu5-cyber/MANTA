"""Local, read-only progress dashboard for the selected MANTA benchmarks."""

from __future__ import annotations

import argparse
import json
import re
import threading
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARKS = ("browsecomp", "workbench", "math500")
LABELS = {
    "browsecomp": "BrowseComp-Plus",
    "workbench": "WorkBench",
    "math500": "MATH-500",
}
BASELINES = {"browsecomp": 76.7, "workbench": 43.3, "math500": 91.1}
START_AT = "2026-10-05T18:00:00+08:00"
TRACE_CACHE: dict[str, tuple[int, int, int, int]] = {}
TRACE_LOCK = threading.Lock()
PARALLEL_GROUPS = {
    "browsecomp": "manta_dsflash_parallel3_20261005_2120",
    "workbench": "manta_dsflash_workbench6_20261005_2145",
    "math500": "manta_dsflash_math6_20261005_2100",
}


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def _tail(path: Path, limit: int = 1000) -> list[str]:
    try:
        with path.open("rb") as handle:
            handle.seek(0, 2)
            size = handle.tell()
            handle.seek(max(0, size - 256_000))
            raw = handle.read()
        return raw.decode("utf-8", errors="replace").splitlines()[-limit:]
    except OSError:
        return []


def _trace_tokens(path: Path) -> tuple[int, int]:
    try:
        stat = path.stat()
    except OSError:
        return 0, 0
    key = str(path)
    with TRACE_LOCK:
        old = TRACE_CACHE.get(key)
        if old and old[:2] == (stat.st_mtime_ns, stat.st_size):
            return old[2], old[3]
    token_in = token_out = 0
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                token_in += int(event.get("token_in") or 0)
                token_out += int(event.get("token_out") or 0)
    except OSError:
        return 0, 0
    with TRACE_LOCK:
        TRACE_CACHE[key] = (stat.st_mtime_ns, stat.st_size, token_in, token_out)
    return token_in, token_out


def snapshot(experiment_id: str) -> dict:
    monitor_dir = ROOT / "artifacts" / "monitor" / experiment_id
    run_root = ROOT / "artifacts" / "full_experiment" / experiment_id
    state = _read_json(monitor_dir / "status.json")
    log_lines = _tail(monitor_dir / "runner.log")
    worker_logs: list[str] = []
    group_states: dict[str, dict] = {}
    rows = []
    total_in = total_out = total_done = total_success = 0
    for benchmark in BENCHMARKS:
        done = success = token_in = token_out = 0
        group_id = PARALLEL_GROUPS[benchmark]
        group_dir = ROOT / "artifacts" / "monitor" / group_id
        manifest = _read_json(group_dir / "manifest.json")
        if manifest:
            group_states[group_id] = _read_json(group_dir / "status.json")
            roots = [
                ROOT / "artifacts" / "full_experiment" / str(worker["experiment_id"])
                for worker in manifest.get("workers", [])
            ]
            if not any(benchmark == b for b in manifest.get("benchmarks", [manifest.get("benchmark")])):
                roots = [run_root]
            if benchmark in ("browsecomp", "workbench", "math500"):
                for worker in manifest.get("workers", []):
                    worker_id = str(worker["experiment_id"])
                    tail = _tail(ROOT / "artifacts" / "monitor" / worker_id / "runner.log", 5)
                    worker_logs.extend(f"[{worker_id[-2:]}] {line}" for line in tail)
        else:
            roots = [run_root]
        for source_root in roots:
            benchmark_root = source_root / benchmark / "self_evolved"
            for eval_path in benchmark_root.glob("*/run_*.eval.json"):
                evaluation = _read_json(eval_path)
                if not evaluation:
                    continue
                done += 1
                success += int(bool(evaluation.get("success")))
                trace_path = eval_path.with_name(eval_path.name.replace(".eval.json", ".trace.jsonl"))
                this_in, this_out = _trace_tokens(trace_path)
                token_in += this_in
                token_out += this_out
        total_in += token_in
        total_out += token_out
        total_done += done
        total_success += success
        rows.append(
            {
                "id": benchmark,
                "label": LABELS[benchmark],
                "done": done,
                "planned": 90,
                "success": success,
                "score": round(100 * success / done, 1) if done else None,
                "paper_score": BASELINES[benchmark],
                "token_in": token_in,
                "token_out": token_out,
            }
        )
    current = ""
    for line in reversed(worker_logs if group_states else log_lines):
        match = re.search(r"RUN_START task_id=([^ ]+) run_index=(\d+)", line)
        if match:
            current = f"{match.group(1)} · 第 {int(match.group(2)) + 1} 次"
            break
    workbench_state = group_states.get("manta_dsflash_workbench6_20261005_2145", {}).get("state")
    if workbench_state in ("running", "recovering"):
        current = "BrowseComp 与 WorkBench 同时运行"
    started = state.get("started_at_utc")
    elapsed_seconds = None
    eta_seconds = None
    if started:
        try:
            elapsed_seconds = max(
                0, int((datetime.now(UTC) - datetime.fromisoformat(started)).total_seconds())
            )
            if total_done > 0 and state.get("state") == "running" and not group_states:
                eta_seconds = int(elapsed_seconds * (90 * len(BENCHMARKS) - total_done) / total_done)
        except ValueError:
            pass
    # These are estimates assuming every input token misses DeepSeek's cache.
    usd_off_peak = (total_in * 0.15 + total_out * 0.60) / 1_000_000
    usd_peak = (total_in * 0.30 + total_out * 1.20) / 1_000_000
    group_failures = [
        f"{group_id}: {group.get('error', '分片失败')}"
        for group_id, group in group_states.items()
        if group.get("state") == "failed"
    ]
    parallel_running = bool(group_states) and state.get("state") == "running"
    recovering = state.get("state") == "failed" and any(
        group.get("state") in ("running", "recovering") for group in group_states.values()
    )
    return {
        "experiment_id": experiment_id,
        "state": "failed" if group_failures else (
            "recovering" if recovering else state.get("state", "scheduled")
        ),
        "message": "; ".join(group_failures) if group_failures else (
            "三项分片继续运行；正式汇总入口待异常记录修复后重启" if recovering else (
                "三项实验运行中；汇总入口等待分片结果" if parallel_running
                else state.get("message", "等待启动")
            )
        ),
        "start_at": state.get("scheduled_at") or START_AT,
        "started_at_utc": started,
        "finished_at_utc": state.get("finished_at_utc"),
        "refreshed_at_utc": datetime.now(UTC).isoformat(),
        "pid": state.get("pid"),
        "current": current,
        "done": total_done,
        "planned": 90 * len(BENCHMARKS),
        "success": total_success,
        "token_in": total_in,
        "token_out": total_out,
        "usd_off_peak": round(usd_off_peak, 4),
        "usd_peak": round(usd_peak, 4),
        "elapsed_seconds": elapsed_seconds,
        "eta_seconds": eta_seconds,
        "benchmarks": rows,
        "logs": (worker_logs + log_lines[-8:])[-40:],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    index = (ROOT / "monitor" / "index.html").read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path in ("/", "/index.html"):
                payload, content_type = index, "text/html; charset=utf-8"
            elif self.path == "/api/status":
                payload = json.dumps(snapshot(args.experiment_id), ensure_ascii=False).encode("utf-8")
                content_type = "application/json; charset=utf-8"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, format: str, *args: object) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"MANTA monitor: http://127.0.0.1:{args.port}/", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
