#!/usr/bin/env python3
"""todoindex - collect TODO/FIXME markers into a markdown table."""
import argparse
import os
import re
import sys

MARK = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b[:\s]*(.*)")
SKIP = {".git", "node_modules", "__pycache__", ".venv", "dist"}


def scan(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    for num, line in enumerate(fh, 1):
                        m = MARK.search(line)
                        if m:
                            yield path, num, m.group(1), m.group(2).strip()
            except OSError:
                continue


def to_markdown(rows):
    out = ["| File | Line | Kind | Note |", "| --- | ---: | --- | --- |"]
    for path, num, kind, note in rows:
        out.append("| %s | %d | %s | %s |" % (path.replace("|", "/"), num, kind,
                                              note.replace("|", "/")[:120]))
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="todoindex", description=__doc__)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    table = to_markdown(list(scan(args.root)))
    if args.out:
        open(args.out, "w", encoding="utf-8").write(table + "\n")
    else:
        print(table)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
