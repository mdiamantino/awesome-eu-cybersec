# Contributing

Thanks for helping build this list. The bar here is deliberately high: every
entry is a claim that a resource exists, is what we say it is, and is relevant to
the EU cybersecurity ecosystem. A contribution is accepted when all three hold.

## The one rule that matters

**Do not add a resource you have not opened.** If you cannot fetch the URL and
see the thing you are describing, the entry does not go in. Unverifiable entries
are worse than missing ones, they cost every future reader time.

## Where to edit

`README.md` is **generated**. Never edit it by hand; your change will be
overwritten on the next build.

The source of truth is `data/resources/<category-slug>.yml`, one file per
category. Add your entry to the right file and run the tooling:

```bash
pip install -r requirements.txt
python scripts/validate.py                  # schema + scope rules
python scripts/check_links.py --only <slug> # fetch the URLs you touched
python scripts/build.py                     # regenerate README.md and the exports
```

Commit the regenerated `README.md`, `data/ecosystem.yml` and
`data/ecosystem.json` along with your data change, CI checks they are in sync.

## Entry format

```yaml
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
```

| Field | Required | Notes |
| --- | --- | --- |
| `name` | yes | The resource's own name. Not a tagline. |
| `url` | yes | HTTPS, canonical, direct. Not a search result. |
| `repo` | no | Source code, when `url` points at docs or an agency page. |
| `description` | yes | **One** objective sentence ending in a full stop, with the EU relevance stated. |
| `subcategory` | yes | Must be declared for the category in `data/categories.yml`. |
| `tags` | yes | 1 to 5 lowercase kebab-case tags. |
| `entry_type` | yes | `Tool`, `Standard`, `Certification Scheme`, `Framework`, `Guideline`, `Report`, `Feed`, `Dataset`, `Training`. |
| `country_or_body` | yes | `Country/Agency` or `EU/Body`, e.g. `France/ANSSI`. |
| `hosting_note` | for tools | `[Open Source]`, `[EU-Hosted]` or `[Commercial]`. Omit for standards and guidelines. |
| `license` | no | SPDX identifier for software. |
| `confidence` | yes | `high` once you have fetched the URL and the content matches. |
| `last_verified` | yes | ISO date you fetched it. |
| `notes` | no | Caveats: superseded document, non-English, archived project, why a commercial entry is here. |

## Scope rules

**1, EU relevance.** The resource must address an EU regulation (NIS2, DORA,
GDPR, CRA, AI Act, eIDAS), an EU or national technical standard or certification
scheme (EUCC, EUCS, SecNumCloud, BSI C5, IT-Grundschutz, ENS), or be maintained
by an official European body, government, university or EU-funded project. An
excellent generic tool with no EU angle does not qualify.

**2, FOSS first.** For tooling, prefer free and open-source software, official
government publications and community-maintained resources. Closed products are
accepted only as sovereign infrastructure or an official registry with no open
equivalent, marked `[Commercial]` with a `notes:` line saying why. This rule does
not apply to standards, schemes and guidance, where "open source" is meaningless.

**3, No pitch.** One objective sentence. No superlatives, no vendor voice. The
validator rejects a list of marketing words outright; the spirit of the rule is
wider than the list.

**4, No dead ends.** A specific URL for the actual resource. Never "search for
X", never a homepage when the resource is three clicks in.

### Out of scope

- Commercial SaaS or consulting with no free tier and no sovereign justification.
- Certification exam prep, job boards, conference listings.
- Generic security tooling with no EU framing.
- Raw legal text with no implementation value, link the ENISA or agency
  implementation guidance instead of the Official Journal PDF, unless the legal
  text itself carries the technical requirements (UN R155 is the usual exception).

### Non-EU entries

A handful of entries come from outside the EU/EEA, UK NCSC guidance, or
international bodies whose output is the operative reference for EU operators.
They are kept only where they are genuinely load-bearing for an EU audience, and
each carries a `notes:` line saying so. New ones need that justification in the PR.

## National authorities

`data/resources/national-authorities.yml` is capped at **four flagship entries
per agency**, enforced by the validator. It is an index of what each authority is
best known for, not a catalogue of everything it has published. Broadening
country coverage is more valuable than deepening one country.

## Review

Pull requests are reviewed against the four scope rules and the verification bar.
Expect to be asked for the evidence you saw on the page. Removals are as welcome
as additions: a link that has rotted, a project that is archived with no
successor, or an entry whose EU framing does not survive scrutiny should be
raised as an issue or a PR.
