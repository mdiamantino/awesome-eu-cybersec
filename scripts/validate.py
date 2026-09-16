#!/usr/bin/env python3
"""Validate data/resources/*.yml against the schema and the list's scope rules.

Run:  python scripts/validate.py
Exit code 1 if any error is found. Warnings do not fail the build.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from collections import defaultdict
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

from common import load_all, load_resource_file, load_schema

# Rule 3 (No-pitch): marketing vocabulary has no place in a description.
BANNED_WORDS = {
    "best", "best-in-class", "cutting-edge", "state-of-the-art", "revolutionary",
    "leading", "world-class", "powerful", "seamless", "robust", "innovative",
    "next-generation", "unparalleled", "comprehensive", "ultimate", "premier",
    "game-changing", "industry-leading", "effortless", "blazing",
}

# Rule 1 (EU relevance): a description that mentions none of these is suspicious.
EU_SIGNALS = (
    "eu", "european", "europe", "enisa", "cert-eu", "nis2", "nis 2", "dora", "gdpr",
    "cra", "cyber resilience act", "eidas", "eucc", "eucs", "gaia-x", "ecsf",
    "secnumcloud", "grundschutz", "ens", "c5", "anssi", "bsi", "csirt", "eudi",
    "member state", "eea", "tiber", "eba", "esma", "eiopa", "ecb", "etsi", "cen",
    "sog-is", "euspa", "esa", "easa", "unece", "horizon", "ecsc",
)

# An entry maintained by an EU/EEA public body satisfies Rule 1 through its
# maintainer, so the description does not have to name a regulation as well.
EU_EEA = {
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark",
    "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
    "Ireland", "Italy", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg",
    "Malta", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden", "EU", "Europe",
}

MAX_PER_AGENCY = 4  # National authorities: flagship only.

# Trailing dots that are not sentence ends. "UN Regulation No. 155" is one entry,
# not two sentences.
ABBREVIATIONS = {
    "no", "nos", "art", "arts", "para", "pt", "vs", "etc", "eg", "ie", "cf",
    "approx", "ca", "ed", "vol", "ch", "sec", "fig", "inc", "ltd", "dr", "prof",
    "st", "mr", "ms", "mrs", "v", "e.g", "i.e",
}


def _has_sentence_break(text: str) -> bool:
    """True if `text` contains a full stop that actually ends a sentence."""
    for match in re.finditer(r"\.\s+(\S)", text):
        following = match.group(1)
        if not following.isupper():
            continue  # "No. 155", "v. 2" and friends
        preceding = re.search(r"([\w.]+)\.$", text[: match.end() - len(match.group(1)) - 1])
        token = preceding.group(1).lower().rstrip(".") if preceding else ""
        if token in ABBREVIATIONS:
            continue
        return True
    return False


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def check_schema(report: Report) -> None:
    schema = load_schema()
    validator = Draft202012Validator(schema)
    for category in load_all()[0]:
        doc = load_resource_file(category)
        for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
            path = "/".join(str(p) for p in err.path) or "<root>"
            report.error(f"{category.path.name}:{path}", err.message)


def check_rules(report: Report) -> None:
    categories, entries_by_slug = load_all()
    today = dt.date.today()

    urls: dict[str, str] = {}
    names: dict[str, str] = {}
    per_agency: dict[str, int] = defaultdict(int)

    for category in categories:
        doc = load_resource_file(category)
        where_file = category.path.name

        if doc.get("category") != category.name:
            report.error(
                where_file,
                f"`category:` is {doc.get('category')!r} but categories.yml says {category.name!r}",
            )

        for entry in entries_by_slug[category.slug]:
            name = entry.get("name", "<unnamed>")
            where = f"{where_file} / {name}"

            # --- uniqueness -------------------------------------------------
            url = entry.get("url", "")
            normalised = url.rstrip("/").lower()
            if normalised in urls:
                report.error(where, f"duplicate URL, already used by {urls[normalised]!r}")
            else:
                urls[normalised] = name

            key = name.strip().lower()
            if key in names:
                report.error(where, f"duplicate name, already used in {names[key]!r}")
            else:
                names[key] = where_file

            # --- taxonomy ---------------------------------------------------
            sub = entry.get("subcategory", "")
            if not category.dynamic and sub not in category.subcategories:
                report.error(
                    where,
                    f"subcategory {sub!r} is not declared for this category "
                    f"(allowed: {', '.join(category.subcategories)})",
                )
            if category.dynamic and "/" not in sub:
                report.error(where, f"subcategory {sub!r} must be 'Country/Agency'")

            # --- description quality (Rule 3, Rule 1) -----------------------
            desc = entry.get("description", "")
            words = {w.strip(".,;:()").lower() for w in desc.split()}
            hits = sorted(words & BANNED_WORDS)
            if hits:
                report.error(where, f"marketing language in description: {', '.join(hits)}")
            if _has_sentence_break(desc):
                report.error(where, "description must be a single sentence")
            maintainer = entry.get("country_or_body", "").split("/", 1)[0].strip()
            if maintainer not in EU_EEA and not any(sig in desc.lower() for sig in EU_SIGNALS):
                report.warn(
                    where,
                    f"neither the description nor the maintainer ({maintainer!r}) "
                    "establishes EU relevance",
                )

            # --- links ------------------------------------------------------
            parsed = urlparse(url)
            if parsed.scheme != "https":
                report.error(where, f"URL must be https, got {parsed.scheme!r}")
            if not parsed.netloc:
                report.error(where, "URL has no host")

            # --- freshness --------------------------------------------------
            raw_date = entry.get("last_verified")
            try:
                verified = dt.date.fromisoformat(str(raw_date))
            except (TypeError, ValueError):
                report.error(where, f"last_verified {raw_date!r} is not an ISO date")
            else:
                if verified > today:
                    report.error(where, f"last_verified {verified} is in the future")
                elif (today - verified).days > 365:
                    report.warn(where, f"last verified {(today - verified).days} days ago")

            # --- FOSS-first (Rule 2) ----------------------------------------
            if entry.get("hosting_note", "").startswith("[Commercial]") and not entry.get("notes"):
                report.warn(
                    where,
                    "commercial entry should carry a `notes:` line justifying it as "
                    "sovereign infrastructure or a registry with no FOSS equivalent",
                )

            if category.slug == "national-authorities":
                per_agency[sub] += 1

    for agency, count in sorted(per_agency.items()):
        if count > MAX_PER_AGENCY:
            report.error(
                "national-authorities.yml",
                f"{agency} has {count} entries, the flagship cap is {MAX_PER_AGENCY}",
            )


def main() -> int:
    report = Report()
    check_schema(report)
    check_rules(report)

    for warning in report.warnings:
        print(f"warning  {warning}")
    for error in report.errors:
        print(f"ERROR    {error}")

    total = sum(len(v) for v in load_all()[1].values())
    print(
        f"\n{total} entries checked - "
        f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
