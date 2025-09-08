#!/usr/bin/env python3
import json
import sys
from typing import TextIO


def print_unique_ids(stream: TextIO) -> int:
    count = 0
    for line in stream:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        uid = obj.get("unique_id")
        if uid is not None:
            print(uid)
            count += 1
    return count


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python display_jsonl_unique_id.py <path-to-jsonl>", file=sys.stderr)
        return 1
    path = argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            printed = print_unique_ids(f)
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        return 3
    return 0 if printed >= 0 else 4


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
