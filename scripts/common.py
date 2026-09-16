"""Shared loading helpers for the awesome-eu-cybersec data files."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESOURCES = DATA / "resources"
CATEGORIES_FILE = DATA / "categories.yml"
SCHEMA_FILE = DATA / "schema.json"


@dataclass(frozen=True)
class Category:
    slug: str
    name: str
    emoji: str
    description: str
    subcategories: tuple[str, ...]
    dynamic: bool

    @property
    def path(self) -> Path:
        return RESOURCES / f"{self.slug}.yml"


def load_categories() -> list[Category]:
    raw = yaml.safe_load(CATEGORIES_FILE.read_text(encoding="utf-8"))
    out = []
    for c in raw["categories"]:
        out.append(
            Category(
                slug=c["slug"],
                name=c["name"],
                emoji=c.get("emoji", ""),
                description=" ".join(c.get("description", "").split()),
                subcategories=tuple(c.get("subcategories") or ()),
                dynamic=bool(c.get("subcategories_are_dynamic")),
            )
        )
    return out


def load_schema() -> dict:
    return json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))


def load_resource_file(category: Category) -> dict:
    if not category.path.exists():
        return {"category": category.name, "entries": []}
    return yaml.safe_load(category.path.read_text(encoding="utf-8")) or {
        "category": category.name,
        "entries": [],
    }


def load_all() -> tuple[list[Category], dict[str, list[dict]]]:
    """Return the taxonomy and a slug -> entries mapping."""
    categories = load_categories()
    entries = {c.slug: (load_resource_file(c).get("entries") or []) for c in categories}
    return categories, entries


def subcategory_order(category: Category, entries: list[dict]) -> list[str]:
    """Declared order for fixed categories; alphabetical for dynamic ones."""
    if not category.dynamic:
        return list(category.subcategories)
    return sorted({e["subcategory"] for e in entries})


def anchor(text: str) -> str:
    """Reproduce GitHub's heading-anchor algorithm.

    Lowercase, drop everything that is not a letter, digit, space, hyphen or
    underscore, then turn spaces into hyphens. Crucially it does NOT trim: an
    emoji-prefixed heading such as "# 🧭 Governance" loses the emoji and keeps
    the space, so GitHub's anchor starts with a hyphen. Trimming here produced
    a table of contents where every category link was silently dead.
    """
    keep = "".join(ch for ch in text.lower() if ch.isalnum() or ch in " -_")
    return keep.replace(" ", "-")
