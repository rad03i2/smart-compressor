from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import CompressionError, compress, extract, inspect_archive


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="smart-compressor", description="Safe local compression toolkit")
    p.add_argument("--version", action="version", version=f"smart-compressor {__version__} — Radwan Abdulhadi Ahmed (@rad03i2)")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("compress", help="compress a file or directory")
    c.add_argument("source")
    c.add_argument("output")
    c.add_argument("--level", type=int, default=6, choices=range(0, 10), metavar="0-9")
    c.add_argument("--overwrite", action="store_true")
    c.add_argument("--json", action="store_true")

    x = sub.add_parser("extract", help="safely extract an archive")
    x.add_argument("archive")
    x.add_argument("destination")
    x.add_argument("--overwrite", action="store_true")
    x.add_argument("--json", action="store_true")

    i = sub.add_parser("inspect", help="show archive statistics without extracting")
    i.add_argument("archive")
    i.add_argument("--json", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "compress":
            info = compress(args.source, args.output, level=args.level, overwrite=args.overwrite)
            data = info.to_dict()
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                saved = max(0, data["unpacked_bytes"] - data["packed_bytes"])
                print(f"Created: {data['path']}\nFormat: {data['format']}\nMembers: {data['members']}\nSaved: {saved} bytes")
        elif args.command == "extract":
            files = extract(args.archive, args.destination, overwrite=args.overwrite)
            if args.json:
                print(json.dumps({"destination": str(Path(args.destination).resolve()), "files": files, "count": len(files)}, indent=2))
            else:
                print(f"Extracted {len(files)} file(s) to {Path(args.destination).resolve()}")
        else:
            data = inspect_archive(args.archive).to_dict()
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print(f"Archive: {data['path']}\nFormat: {data['format']}\nMembers: {data['members']}\nPacked: {data['packed_bytes']} bytes\nUnpacked: {data['unpacked_bytes']} bytes\nRatio: {data['ratio']:.2%}")
        return 0
    except (CompressionError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
