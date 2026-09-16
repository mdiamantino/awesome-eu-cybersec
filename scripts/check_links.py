#!/usr/bin/env python3
"""Fetch every URL in the list and report the ones that no longer resolve.

Run:  python scripts/check_links.py [--only <category-slug>] [--concurrency 8]
      python scripts/check_links.py --json report.json

A HEAD request is tried first; hosts that reject HEAD are retried with a ranged
GET. Agency sites frequently sit behind bot protection, so 403 and 405 are
reported separately from genuine breakage and do not fail the run.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from dataclasses import asdict, dataclass

# Runnable from anywhere: CONTRIBUTING tells contributors to use
# `python scripts/validate.py` from the repo root, which puts the repo root on
# sys.path rather than this directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import httpx

from common import load_all

# Several agency sites (bsi.bund.de, ccn-cert.cni.es) answer a bare HEAD with a
# 400 or 500 and serve the same URL over GET, so a browser UA plus a GET retry is
# the difference between a clean report and a wall of false failures.
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
# Not breakage: the resource is there, the crawler is being turned away.
SOFT_STATUSES = {401, 403, 405, 406, 429}


@dataclass
class Result:
    name: str
    url: str
    category: str
    status: int | None
    note: str

    @property
    def state(self) -> str:
        if self.status is not None and 200 <= self.status < 400:
            return "ok"
        if self.status in SOFT_STATUSES:
            return "blocked"
        return "broken"


async def check(client: httpx.AsyncClient, entry: dict, category: str, sem: asyncio.Semaphore) -> Result:
    url = entry["url"]
    async with sem:
        for method in ("HEAD", "GET"):
            try:
                headers = {"Range": "bytes=0-2047"} if method == "GET" else {}
                response = await client.request(method, url, headers=headers)
            except httpx.HTTPError as exc:
                if method == "GET":
                    return Result(entry["name"], url, category, None, type(exc).__name__)
                continue
            if method == "HEAD" and not (200 <= response.status_code < 400):
                continue  # retry over GET before believing a HEAD failure
            return Result(entry["name"], url, category, response.status_code, "")
    return Result(entry["name"], url, category, None, "unreachable")


async def run(only: str | None, concurrency: int) -> list[Result]:
    categories, entries_by_slug = load_all()
    targets = [
        (entry, c.name)
        for c in categories
        if only in (None, c.slug)
        for entry in entries_by_slug[c.slug]
    ]
    sem = asyncio.Semaphore(concurrency)
    limits = httpx.Limits(max_connections=concurrency)
    async with httpx.AsyncClient(
        follow_redirects=True, timeout=30.0, headers={"User-Agent": UA}, limits=limits, verify=True
    ) as client:
        return await asyncio.gather(*(check(client, e, c, sem) for e, c in targets))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="limit to one category slug")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--json", dest="json_out", help="write the full report here")
    parser.add_argument(
        "--fail-on-blocked", action="store_true", help="treat 403/405 as failures too"
    )
    args = parser.parse_args()

    results = asyncio.run(run(args.only, args.concurrency))
    broken = [r for r in results if r.state == "broken"]
    blocked = [r for r in results if r.state == "blocked"]

    for r in sorted(blocked, key=lambda r: r.url):
        print(f"blocked  {r.status or r.note:>12}  {r.name} - {r.url}")
    for r in sorted(broken, key=lambda r: r.url):
        print(f"BROKEN   {r.status or r.note:>12}  {r.name} - {r.url}")

    print(
        f"\n{len(results)} links: {len(results) - len(broken) - len(blocked)} ok, "
        f"{len(blocked)} blocked by bot protection, {len(broken)} broken"
    )

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump([{**asdict(r), "state": r.state} for r in results], f, indent=2)

    if broken:
        return 1
    return 1 if (args.fail_on_blocked and blocked) else 0


if __name__ == "__main__":
    sys.exit(main())
