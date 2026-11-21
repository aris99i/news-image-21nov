#!/usr/bin/env python3
"""Write the entry image to the output directory (deterministic copy).

After copying, the output is verified against the source by sha256; a
mismatch exits 1 so a bad run never passes as a good one.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    src = HERE / "entry.png"
    dst = OUT / "entry.png"
    shutil.copyfile(src, dst)
    if sha256(src) != sha256(dst):
        print("error: output sha256 does not match entry.png", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
