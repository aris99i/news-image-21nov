#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261121 bounty.

Copies the pre-rendered front page (entry.png, produced by draw_news.py)
into the output directory the grader provides, so the judge receives the
image at $MAKEFUN_OUTPUT_DIR/entry.png. Standard library only.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    if sha256_of(SOURCE) != sha256_of(dest):
        print("error: sha256 mismatch after copy", file=sys.stderr)
        return 1
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
