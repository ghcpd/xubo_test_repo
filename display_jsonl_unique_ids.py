#!/usr/bin/env python3
import argparse
import json
import sys
from typing import TextIO


def iter_jsonl(stream: TextIO):
    for line_no, line in enumerate(stream, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            yield line_no, json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON on line {line_no}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Display the value of a key (default: unique_id) from each row in a JSONL file."
    )
    parser.add_argument("path", help="Path to the JSONL file")
    parser.add_argument(
        "-k",
        "--key",
        default="unique_id",
        help="Key to extract from each JSON object (default: unique_id)",
    )
    args = parser.parse_args()

    try:
        with open(args.path, "r", encoding="utf-8") as f:
            for line_no, obj in iter_jsonl(f):
                value = obj.get(args.key)
                if value is not None:
                    print(value)
                else:
                    # Skip lines without the key, but inform via stderr
                    print(
                        f"Warning: key '{args.key}' not found in line {line_no}",
                        file=sys.stderr,
                    )
    except FileNotFoundError:
        print(f"File not found: {args.path}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error opening file {args.path}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
