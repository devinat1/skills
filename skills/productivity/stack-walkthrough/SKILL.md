---
name: stack-walkthrough
description: Explore a PR stack, connect each PR to available results, and ask one question at a time to decide what to keep, change, or remove. Use for an interactive stack walkthrough before implementation.
---

# Stack walkthrough

Explore the whole stack first. Then use `/statement-walkthrough`, with each PR as one statement, to decide what to keep, change, or remove. Record changes for a later implementation pass. This skill does not implement them.

## 1. Explore before interviewing

Read repository instructions and inspect working-tree status. Establish the ordered stack from Graphite metadata or Git ancestry, using the user's base and tip when supplied. Resolve PR numbers, links, titles, parents, and commit IDs through available read-only tools. Ask about the stack path only when it is ambiguous. Use the existing checkout; fetching, pulling, and switching branches are separate actions, not prerequisites for this walkthrough.

Work bottom-up through **every PR's actual diff against its stack parent**, plus the relevant surrounding code. Titles and file statistics are not enough. Inspect integration at the tip to identify replacements, shared dependencies, and behavior introduced only by later PRs. Keep each PR's own changes distinct from its final behavior at the tip.

Find the available results that bear on those changes: experiment reports, raw outputs, action traces, logs, test results, or other recorded outcomes. For each PR, retain a compact internal map of purpose, concrete changes, dependencies, evidence, limitations, and unresolved facts. Preparation is complete when every PR has this map, including explicit evidence gaps. Give brief progress updates during a long inspection. Start the decision interview only after this pass.

Keep a resumable checkpoint under `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/stack-walkthrough/<unique-run-id>/walkthrough.md`. Record repository, base, tip, ordered branches and commits, evidence locations, current PR, addressed PRs, retained decisions, open questions, and the numbered change backlog. This is workflow state, not personal memory. If a stricter active workflow prohibits checkpoint writes, retain session state and say that no disk checkpoint was saved. On resume, check for changed commits and flag stale explanations.

## 2. Hand each PR to the statement walk

Say that `/statement-walkthrough` is being used to decide one PR at a time. Follow that skill. Each PR is one statement, in stack order. Do not split a PR into smaller statements. Write into this skill's checkpoint. This skill owns the visible finish. Do not show `statement-walkthrough` completion suggestions.

The explanation for the current PR statement is:

- **PR i of N — title / branch**, with its PR link when available.
- **What it does:** its purpose and two or three concrete behavior changes. Describe actual scope even when the title understates it.
- **What happened:** the relevant observed result, its conditions, and the supported explanation. Link the evidence where useful.
- **Decision-relevant limit:** the caveat, implementation issue, or dependency the user needs to assess this PR.

For an experiment, use a concrete account such as: "In [run], [scraper] copied X of Y complete articles under [defense], compared with Z without it. The trace shows [action]; the implementation permits it because [mechanism]." Use this shape only when those facts are supported. For an infrastructure PR, explain what it measures or enables and how later results use it; do not invent an isolated effectiveness result.

Match evidence to the actual implementation, dataset, configuration, scoring rule, and recorded revision. Distinguish a PR's scraper from a later replacement and archived observations from fresh validation. State denominators, time/request limits, and the definition of success when they change the meaning. Missing trials and infrastructure failures are not zero recovery. Copied or resumed results are not independent repetitions. Test sources alone do not establish that tests passed.

A proposed mechanism needs both code and execution evidence to be presented as an observed explanation. Otherwise label it an inference or say the cause is unknown. A lower score alone does not show that a detector fired. Separate a broken implementation from a weak mechanism that the scraper satisfied as designed. Report missing evidence directly; running experiments or tests is outside this read-only walkthrough.

A keep, change, or remove decision does not authorize closing PRs, dropping commits, or deleting history. Identify shared code still needed by retained functionality before proposing deletion boundaries. Ask only about newly unresolved choices.

## 3. Finish the walkthrough

Keep application code, Git state, PRs, and experiment artifacts unchanged throughout the walkthrough. Only the permitted external checkpoint/backlog may be written. Implementation requires a separate request and any applicable approval workflow.

After the statement walk advances past the final PR, show the complete deduplicated change backlog, retained decisions, and unresolved questions. Distinguish "addressed in discussion" from "implemented." Report the checkpoint path, or the lack of a disk checkpoint, and stop. If another explicitly invoked workflow requires a plan handoff, follow its rules after the interview; this skill itself does not impose a planning tool or start implementation.
