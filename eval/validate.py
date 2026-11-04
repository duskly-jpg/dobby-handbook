#!/usr/bin/env python3
"""DobbyEval dataset validator — CI gate for eval/dobbyeval_v0.json.

Asserts structure and integrity of the eval set with hard evidence
(exit non-zero on any violation). No network, stdlib only.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "eval" / "dobbyeval_v0.json"

META_REQUIRED = ("name", "domain", "created", "scoring", "usage", "baseline")
TASK_REQUIRED = ("id", "cat", "scenario", "ask", "gold", "reflect")

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def main() -> int:
    raw = EVAL.read_bytes()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"FAIL: invalid JSON: {e}")
        return 1
    print(f"ok: JSON parses ({len(raw)} bytes)")

    if not isinstance(data, dict):
        err(f"root must be object, got {type(data).__name__}")
        return report()

    meta = data.get("_meta")
    if not isinstance(meta, dict):
        err("_meta must be object")
    else:
        for k in META_REQUIRED:
            v = meta.get(k)
            if not isinstance(v, str) or not v.strip():
                err(f"_meta.{k} must be non-empty string")
        print("ok: _meta fields" if not errors else f"meta errors so far: {len(errors)}")

    cats = data.get("trap_categories")
    if not isinstance(cats, list) or not cats or not all(isinstance(c, str) and c.strip() for c in cats):
        err("trap_categories must be non-empty list of non-empty strings")
    else:
        print(f"ok: trap_categories ({len(cats)} categories)")

    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        err("tasks must be non-empty list")
        return report()

    seen_ids: set[str] = set()
    cat_set = set(cats) if isinstance(cats, list) else set()
    for i, t in enumerate(tasks):
        if not isinstance(t, dict):
            err(f"tasks[{i}] must be object")
            continue
        for k in TASK_REQUIRED:
            v = t.get(k)
            if not isinstance(v, str) or not v.strip():
                err(f"tasks[{i}].{k} must be non-empty string")
        tid = t.get("id")
        if isinstance(tid, str):
            if tid in seen_ids:
                err(f"duplicate task id: {tid}")
            seen_ids.add(tid)
        if t.get("cat") not in cat_set:
            err(f"tasks[{i}].cat {t.get('cat')!r} not in trap_categories")

    print(f"ok: tasks ({len(tasks)} tasks, ids unique)")

    # cross-check declared count if present
    declared = meta.get("task_count") if isinstance(meta, dict) else None
    if declared is not None and declared != len(tasks):
        err(f"_meta.task_count={declared} != actual {len(tasks)}")

    return report()


def report() -> int:
    if errors:
        print(f"FAIL: {len(errors)} violation(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS: dobbyeval_v0.json valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
