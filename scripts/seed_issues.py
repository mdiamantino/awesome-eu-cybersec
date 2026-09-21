"""Turn the gaps in .github/seed-issues.yml into GitHub issues.

A contributor who lands on "contributions welcome" leaves. A contributor who
lands on "Belgium has no CCB entry, here is the file, here is the format, here is
the command that checks your work" opens a pull request. This script renders the
second kind of issue, one per gap, and creates them through the `gh` CLI.

    python3 scripts/seed_issues.py              # print what would be created
    python3 scripts/seed_issues.py --full       # print the rendered bodies too
    python3 scripts/seed_issues.py --create     # create the labels and the issues

Existing open issues with the same title are skipped, so a re-run tops up rather
than duplicating.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml

from common import ROOT

SEEDS = ROOT / ".github" / "seed-issues.yml"

ENTRY_EXAMPLE = """```yaml
- name: Vulnerability-Lookup
  url: https://github.com/vulnerability-lookup/vulnerability-lookup
  description: Software from CIRCL Luxembourg that correlates advisories from national
    vulnerability databases and CSAF providers and supports coordinated disclosure workflows.
  subcategory: Vulnerability Intelligence
  tags: [cvd, correlation, circl]
  entry_type: Tool
  country_or_body: Luxembourg/CIRCL
  hosting_note: '[Open Source]'
  license: AGPL-3.0-or-later
  confidence: high
  last_verified: '2026-09-16'
```"""

HOW_TO = """### How to do it

```bash
git clone https://github.com/{repo} && cd awesome-eu-cybersec
make install
$EDITOR {path}
make build     # regenerates README.md and the exports
make check     # the same thing CI runs
```

Commit the YAML change together with the regenerated `README.md`,
`data/ecosystem.yml` and `data/ecosystem.json`, then open the pull request.

### Entry format

{example}

Field reference and the scope rules are in
[CONTRIBUTING.md](https://github.com/{repo}/blob/main/CONTRIBUTING.md).

### The one bar

Open the URL yourself and confirm the page is what you say it is. An entry you
have not read does not go in, and `confidence: high` means you fetched it.
Quote what you saw in the pull request.

Not sure whether something qualifies? Ask in this issue before writing the entry.
That is what it is for."""

COUNTRY_BODY = """`data/resources/national-authorities.yml` currently has **{have}** for
{country}.

This section is an index of what each national authority is best known for: the
standards, frameworks and guidance an operator in that country actually has to
work against. The cap is four flagship entries per agency, so depth is not the
goal, presence is.

### What is wanted

One to four entries for {agency_clause}. Good candidates are the
national cybersecurity framework or baseline, NIS2 transposition guidance for
operators, an incident reporting procedure, or a widely used technical
publication series.

In this file `subcategory` is the agency itself, written `Country/Agency`, for
example `{country}/CCB`, and `country_or_body` matches it. The validator enforces
that shape.

Confirm the body still exists under that name and find its current canonical
URL: the hint above is a starting point, not a verified fact. National-language
sources are fine and often better, add a `notes:` line saying which language.

{how_to}"""

TOPIC_BODY = """{detail}

### What is wanted

Entries in `{path}`{subcategory_clause}. One good entry is a complete
contribution; there is no need to fill the whole gap.

{how_to}"""


def run(args: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(args, text=True, capture_output=True, **kw)


def existing_titles(repo: str) -> set[str]:
    proc = run(["gh", "issue", "list", "--repo", repo, "--state", "all",
                "--limit", "500", "--json", "title"])
    if proc.returncode != 0:
        print(proc.stderr.strip(), file=sys.stderr)
        return set()
    return {i["title"] for i in json.loads(proc.stdout or "[]")}


def render(seeds: dict, repo: str) -> list[dict]:
    issues = []

    for c in seeds.get("countries") or []:
        path = "data/resources/national-authorities.yml"
        have = "no entries" if not c["have"] else f"{c['have']} entry"
        agency = c.get("agency") or "the national cybersecurity authority"
        issues.append(
            {
                "title": f"{c['country']}: add the national cybersecurity authority's flagship publications",
                "labels": ["country gap", "good first issue", "help wanted"],
                "body": COUNTRY_BODY.format(
                    have=have,
                    country=c["country"],
                    agency_clause=agency,
                    how_to=HOW_TO.format(repo=repo, path=path, example=ENTRY_EXAMPLE),
                ),
            }
        )

    for t in seeds.get("topics") or []:
        slug = t.get("file")
        path = f"data/resources/{slug}.yml" if slug else "data/resources/"
        sub = t.get("subcategory")
        issues.append(
            {
                "title": t["title"],
                "labels": list(t.get("labels") or ["coverage gap", "help wanted"]),
                "body": TOPIC_BODY.format(
                    detail=" ".join((t.get("detail") or "").split()),
                    path=path,
                    subcategory_clause=f", subcategory `{sub}`" if sub else "",
                    how_to=HOW_TO.format(repo=repo, path=path, example=ENTRY_EXAMPLE),
                ),
            }
        )

    return issues


def ensure_labels(seeds: dict, repo: str) -> None:
    for label in seeds.get("labels") or []:
        proc = run(["gh", "label", "create", label["name"], "--repo", repo,
                    "--color", label["color"],
                    "--description", label.get("description", ""), "--force"])
        status = "ok" if proc.returncode == 0 else proc.stderr.strip()
        print(f"label {label['name']}: {status}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default="mdiamantino/awesome-eu-cybersec")
    ap.add_argument("--create", action="store_true", help="actually create them")
    ap.add_argument("--full", action="store_true", help="print rendered bodies")
    ap.add_argument("--limit", type=int, default=0, help="stop after N issues")
    args = ap.parse_args()

    seeds = yaml.safe_load(SEEDS.read_text(encoding="utf-8"))
    issues = render(seeds, args.repo)
    if args.limit:
        issues = issues[: args.limit]

    if not args.create:
        for i in issues:
            print(f"- {i['title']}  [{', '.join(i['labels'])}]")
            if args.full:
                print("\n" + i["body"] + "\n" + "-" * 72)
        print(f"\n{len(issues)} issues would be created in {args.repo}.")
        print("Re-run with --create to create them.")
        return 0

    if run(["gh", "auth", "status"]).returncode != 0:
        print("gh is not authenticated: run `gh auth login` first.", file=sys.stderr)
        return 1

    ensure_labels(seeds, args.repo)
    seen = existing_titles(args.repo)
    created = 0
    for i in issues:
        if i["title"] in seen:
            print(f"skip (exists): {i['title']}")
            continue
        cmd = ["gh", "issue", "create", "--repo", args.repo,
               "--title", i["title"], "--body", i["body"]]
        for label in i["labels"]:
            cmd += ["--label", label]
        proc = run(cmd)
        if proc.returncode == 0:
            created += 1
            print(f"created: {proc.stdout.strip()}")
        else:
            print(f"failed: {i['title']}: {proc.stderr.strip()}", file=sys.stderr)
    print(f"\n{created} issue(s) created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
