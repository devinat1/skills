---
name: research-idea-brief
description: "Turn a research or product idea into a concise four-section brief: problem, prior work, remaining gap, and proposed approach. Use when the user asks to package, frame, structure, or write up an idea, research direction, benchmark proposal, or gap analysis in this format."
---

# Research Idea Brief

Create a concise, evidence-aware brief that makes one idea legible without overstating novelty.

## Workflow

1. Identify one atomic idea. If the request contains multiple independent ideas, produce separate briefs or ask which one to prioritize.
2. State the target problem precisely: who experiences it, why current practice fails, why it matters now, and what outcome would benefit them. Explain the stakes in language the intended audience understands.
3. Summarize the strongest relevant prior work supplied by the user or already verified in the conversation. If it is missing and the user wants a research claim, run focused Consensus MCP searches first, using specific academic query terms; cite only returned papers whose metadata or abstracts support the claim. Use other sources only to cover work Consensus does not index; do not invent citations or novelty claims.
4. Define the remaining gap narrowly. Distinguish a research gap from an implementation detail or a product feature.
5. Propose the minimum approach that tests or addresses the gap. Explain why it might work; include the setting, comparison or baseline, observable outcome, and a result that would weaken the idea. Keep the storyline aligned with the actual proposed work when the project changes.

## Output format

Use exactly these headings and write one compact paragraph under each:

**What is the Problem?** Explain the concrete limitation, stakes, and affected user or research setting.

**What has been done already to address this problem?** Name the closest verified approaches, benchmarks, systems, or papers and say what each establishes.

**What is the gap that still remains?** State the narrow unaddressed question. Do not call it novel unless sources support that claim.

**How do you propose to address this gap?** Describe the smallest credible study, benchmark, system, or intervention, including what would be measured or compared.

Then add a short `## References` list only for sources actually provided or verified.

## Quality bar

- Prefer specific verbs and measurable claims over vague qualifiers like “efficient” or “robust”; call an unmeasured improvement a hypothesis.
- Do not equate passing a benchmark with broad real-world capability without explaining the benchmark oracle and its limits.
- Keep the proposal falsifiable: name what result would support or weaken it.
- Preserve uncertainty where prior work is incomplete, conflicting, or recent. Never present a workshop anecdote, unverified citation, or unsourced novelty claim as established fact.
- Do not write an implementation plan, grant proposal, or literature review unless the user asks for one.


## Incentive-check integration

At the stage described below, read `${AGENTIC_HOME:-$HOME/.agentic}/skills/incentive-check/INTEGRATIONS.md` and use **Run** mode. Before drafting, when the framing materially relies on a named outsider's public forecast or endorsement, check that one statement. Keep methodological results and novelty claims governed by their source evidence. Use a qualified observation or citation within the existing four-section brief rather than adding a fifth section.

## Automatic Jev check

Read `${AGENTIC_HOME:-$HOME/.agentic}/artifacts/jev/PROTOCOL.md` and use its shared helper; do not duplicate or replace it. Run automatically only when the named bounded subtask and minimized evidence with stable source IDs exist; otherwise record `not_applicable` and do not manufacture work. Form and retain the ordinary preliminary evidence judgment first. For a draft claim and verified passage, ask Choice `supports`/`contradicts`/`unclear`, requiring scope and qualifications. Main agent selects work and writes the brief; Jev cannot establish novelty.

An `unclear` result means the evidence does not decide the bounded question.

Jev is advisory: main agent retains retrieval, explanations, generation, deterministic rules, and approvals. Record invoked checks privately per the protocol. If unavailable, ambiguous, `none_fit`, or conflicting with preliminary evidence, use the original workflow; where allowed, say once: `Jev check unavailable; used the existing review process.` Never suppress an evidence-backed finding because Jev disagrees. Probabilities and scores are not thresholds or permissions and never authorize a message, edit, installation, purchase, upload, activation, or other side effect.
