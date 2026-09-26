---
name: paper-submission-audit
description: Audit a research-paper draft and its target venue for writing, evidence, presentation, and submission-readiness problems. Use when checking a paper before submission; audit only, no rewriting or submitting.
---

# Paper submission audit

## Inputs

Ask for the draft (or readable path), target venue and submission cycle, and any separate figures, references, or submission artifacts. If a draft is unavailable, audit only supplied material and label the rest unchecked. If the venue is unknown, perform a manuscript-only audit; do not infer a conference's rules.

## Audit

1. Read the actual draft, abstract, figures/tables, bibliography and artifacts that are available. Evaluate why the problem matters, prior-work positioning, gap, approach, evidence, and consistency between claims and results. Assess the abstract/introduction using APSET: area, problem, *our system*, evaluation, takeaway. Treat sentence counts (roughly 1/1/2–3/2/1) as guidance, not a rigid quota. Distinguish planned evaluation from observed results.
2. For security work, check attacker goal, capabilities, knowledge/assumptions, scope/exclusions, and whether the threat model is plausible. Flag unsupported adjectives such as “efficient” and “robust”; ask for quantities and precise verbs. Check figure/table reference order, visual legibility at final size, consistent component names, informative captions, consistent headings, verified citation metadata, and widows/orphans or awkward breaks **only where the rendered document can actually be inspected**. Check grayscale and printed-size readability only when a rendered artifact or printout is accessible.
3. Fetch the **official CFP and submission instructions for the exact venue and cycle**. Separately list confirmed abstract, registration, full-paper, artifact and post-submission deadlines; author-account/identifier requirements, formatting, and subsequent actions. Check again near the deadline because rules can change. Never generalize another venue's arXiv/ORCID or author-ID rules from a workshop anecdote; do not conflate those identifiers. If official sources are inaccessible, mark every venue-specific check unverified. Do not guess a deadline.
4. Check whether collaborators have time to review; about a week before the deadline is a planning heuristic, not an enforced rule. Do not create an account, modify a submission, or submit anything.

## Output

List prioritized findings with manuscript location, evidence (draft excerpt or official URL), impact, and concrete fix to make. Separate **confirmed issues**, **recommendations**, and **unverified checks**. Include the official source and access date for venue rules. If there is no supplied PDF, no rendered figure, or no full reference metadata, name exactly what could not be checked. End after the audit; do not rewrite the paper.
