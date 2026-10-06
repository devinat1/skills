---
name: field-snapshot
description: Produce a standalone, source-backed snapshot of a research area's recent venue programs, active researchers and groups, trends, and up to ten papers to read. Use for field updates, not idea-specific prior-work reviews.
---

# Research field snapshot

Ask for the research area, relevant venues, and time window only where not supplied. Default to recent completed cycles of the leading venues relevant to the named area; state the dates and chosen venues. A single report is sufficient: no saved baseline, scheduled run, or automatic alerts.

1. Inspect official programs, proceedings, and paper pages for the selected cycles. Record coverage: which venues/cycles were checked and which were inaccessible. Identify recurring groups and authors (including students where public records support it), citing evidence; do not equate publication count with research quality.
2. Describe themes across the surveyed papers. Claim a topic is growing or shrinking only when comparable counts or clearly specified evidence across equivalent cycles support it; give the denominator and caveats. Otherwise describe it as an observation, not a trend.
3. Select **up to ten** papers for reading because they illuminate methods, important problems, or boundaries in the area. Give citation/link and one concrete reason per selection. Do not pad to ten, misstate unread abstracts as full-paper findings, or invent a ranking of importance.

Return a dated standalone report: scope/coverage, observed themes and evidence-qualified trends, active groups/authors, reading selections, and gaps/limits. Source each material claim; if retrieval is unavailable, stop with the uncovered scope rather than manufacturing a snapshot. This skill does not review one idea's prior work (`/literature-review`), decide novelty, compare to older reports, configure alerts, or save the results unless separately requested.

## Incentive-check integration

At the stage described below, read `${AGENTIC_HOME:-$HOME/.agentic}/skills/incentive-check/INTEGRATIONS.md` and use **Follow-up** mode. When the user asks who benefits from a selected named author's public claim, hand off the exact claim and source to a separate incentive-check. Preserve the standalone field report, source coverage, and reading-selection criteria. Do not append an incentive block, create files, or add monitoring to the ordinary snapshot.
