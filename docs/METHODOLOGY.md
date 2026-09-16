# Methodology

How entries get into this list, and what "verified" means here.

## Sourcing

Candidates are gathered one category and subcategory at a time from the
publication catalogues of EU bodies and national agencies, the repository
organisations those bodies maintain, EU research-project registries such as
CORDIS, and the standards bodies that serve EU regulation.

Every sweep works from the same written brief: the scope rules in
[`CONTRIBUTING.md`](../CONTRIBUTING.md). Coverage is therefore comparable across
categories, and a subcategory with few genuinely qualifying resources stays
short rather than being padded to look even.

## Verification

Every candidate goes through the same gate:

1. **Deduplicate by URL**, normalised for trailing slashes and case.
2. **Fetch the URL** and compare the page or document against the claim. A page
   that loads but describes something else is a failure, not a pass. PDFs are
   checked by extracting the cover page, not by trusting the filename.
3. **Discard on any mismatch.** Wrong issuer, wrong document, redirect to a
   generic landing page, or a description the page does not support: the entry
   is dropped rather than softened.
4. **Raise confidence to `high`** only for entries whose URL was fetched and
   whose content matched the claim, and whose EU relevance and maintainer are
   established by the page itself rather than inferred from the domain name.
   Everything else stays `medium` and renders with a ⚠️ marker.

Entries blocked by robots rules or bot protection are discarded rather than
inferred from search-result snippets.

## Critic pass

The verified, deduplicated set is re-read against the scope rules, looking for:

- descriptions that overstate what the fetched page actually establishes;
- entries whose EU relevance is assumed from a domain name rather than shown;
- marketing language that survived the first pass;
- tools marked `[Open Source]` with no licence evidence;
- `entry_type` that does not match what the resource is, such as a CTF challenge
  archive is a dataset, not a tool.

Entries with a fixable description are corrected and kept. Entries with an
identity or issuer mismatch are removed.

## Continuous checks

CI runs three gates on every pull request:

| Gate | What it enforces |
| --- | --- |
| `scripts/validate.py` | JSON Schema, taxonomy, duplicate URLs and names, one-sentence descriptions, banned marketing vocabulary, `hosting_note` on tools, the four-per-agency flagship cap, future or stale `last_verified` dates. |
| `scripts/build.py --check` | `README.md` and the exports match the data. Nobody hand-edits the generated list. |
| `scripts/check_links.py` | Every URL still resolves. HEAD first, GET on fallback, because several agency sites answer a bare HEAD with a 400. Also reports URLs that redirect elsewhere, since two spellings of one ENISA page previously entered the list as separate entries. |

Two entries redirect on purpose and are left alone: the Italian TIBER-IT page
bounces through Radware bot protection rather than having moved, and the Dutch
telecom decree redirects from its stable `BWBR` permalink to a dated
consolidation that will itself age out.

The link check also runs weekly on a schedule, so rot surfaces as an issue rather
than as a reader's dead end.

## Known limitations

- **Coverage is uneven by design.** Sparse subcategories were not padded. Where
  few resources genuinely qualify, few are listed.
- **Bot protection skews coverage.** Some national agency sites (notably several
  Belgian and Spanish ones) block automated fetching. Resources behind them are
  under-represented, not absent from the ecosystem. Contributions from people who
  can verify them by hand are especially welcome.
- **`medium` confidence is real uncertainty.** It usually means the resource
  exists and resolves, but its EU framing or its maintenance status rests on
  weaker evidence than we would like.
- **Licence metadata is incomplete.** Where a tool lives in a single GitHub
  repository, its SPDX identifier is read from the GitHub API rather than
  assumed. Where it lives on a project website, a research page or an agency
  portal, the licence is documented on the site but not machine-readable, and
  the entry has no `license` field yet. `scripts/validate.py` warns on each one;
  the warnings are a contribution backlog, not noise to be silenced. Three
  repositories publish no licence file at all and say so in their `notes`.

- **Language.** English pages are preferred where an agency publishes both, but
  many national standards exist only in the national language. Those entries are
  tagged with the language rather than excluded.
