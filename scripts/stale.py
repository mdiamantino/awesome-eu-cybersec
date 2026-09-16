#!/usr/bin/env python3
"""List entries whose `last_verified` date has aged out.

Run:  python scripts/stale.py [--days 365]

Verification is a claim with a shelf life: agency sites reorganise, PDFs move,
projects get archived. This prints the oldest first so re-checking has an order.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys

from common import load_all


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=365)
    args = parser.parse_args()

    today = dt.date.today()
    rows = []
    for category, entries in zip(*_paired()):
        for entry in entries:
            try:
                verified = dt.date.fromisoformat(str(entry.get("last_verified")))
            except (TypeError, ValueError):
                rows.append((9999, category, entry["name"], "no valid date"))
                continue
            age = (today - verified).days
            if age > args.days:
                rows.append((age, category, entry["name"], verified.isoformat()))

    rows.sort(reverse=True)
    for age, category, name, when in rows:
        print(f"{age:>5}d  {category:<45}  {name}  (last verified {when})")

    print(f"\n{len(rows)} entries not verified in the last {args.days} days")
    return 0


def _paired():
    categories, entries_by_slug = load_all()
    return [c.name for c in categories], [entries_by_slug[c.slug] for c in categories]


if __name__ == "__main__":
    sys.exit(main())
