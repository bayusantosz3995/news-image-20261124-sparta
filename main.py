#!/usr/bin/env python3
"""Entrypoint for the news-image-20261124 make.fun entry (Sparta).

Copies the pre-rendered timeline image (entry.png, drawn by draw.py)
to the grader's output directory. Standard library only, so it runs
in the grader's pinned image with no PIL and no fonts installed:
the same bytes are written on every run, deterministically.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        print("entry.png missing from repo", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    # The grader runs the program twice and both runs must write the
    # same bytes, so confirm the copy is complete.
    if os.path.getsize(dst) != os.path.getsize(src):
        print("short copy", file=sys.stderr)
        return 1
    print(f"wrote entry.png ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
