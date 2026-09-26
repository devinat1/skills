---
name: apset
description: Organizes current work into APSET (Area, Problem, System, Evaluation, Takeaway) through a clarify-style interview. Use when the user explicitly asks for an APSET, says "/apset", or says "organize this with APSET".
---

# APSET

## Consequential advice

When the user is stuck on a consequential decision, follow the `Advice gate`
in `dissenter` before giving a recommendation.
When the gate applies, first say that you are using `/dissenter` and why.

Help organize what the user is working on into the APSET format through natural collaborative dialogue.

Start by understanding the current project context, then interview one APSET section at a time. Keep interviewing until each section is concrete enough to act on — then output a brief APSET document and stop.

<HARD-GATE>
Do NOT write code, edit files, scaffold projects, produce implementation plans, write design docs, commit specs, or invoke writing-plans. This skill ends with a brief APSET markdown document in chat.
</HARD-GATE>

## Checklist

Complete these in order:

1. **Explore project context** — check files, docs, recent commits, and the current conversation
2. **Scope check** — if the work spans multiple independent threads, flag it and APSET one slice at a time
3. **Interview one APSET section at a time** — one question per turn; use the four storyline questions to sharpen the problem and motivate the proposed work, not as a mapping of prior work to System or gap to Evaluation
4. **Threat model when security is relevant** — probe System until attacker goal, capabilities, knowledge/assumptions, and scope/exclusions are concrete
5. **Stop when thorough** — each section survives "what about when…?"; shallow one-liners mean keep asking
6. **Deliver brief APSET doc** — markdown sections in chat; no preamble beyond the doc itself

## Question discipline

Before the first interview question, say that you are using `/clarify`'s
interview style to structure the APSET questions.

Follow the same interview style as [`skills/productivity/clarify/SKILL.md`](../../productivity/clarify/SKILL.md):

- **One question per message** — break multi-part topics across turns
- **Multiple choice preferred** when it speeds answers; open-ended when needed
- **Explore the codebase** when a question can be answered from the repo instead of asking the user
- **Go deep on branches** — gaps and assumptions often hide in edge cases

Do not lead with recommended answers. Draw the user's thinking out with questions. If they are stuck, a short recommendation is fine — then return to asking.

## Storyline questions

Use these to test motivation one at a time; `/research-idea-brief` owns the four-question prior-work/gap brief:

1. What problem matters, to whom, and why now?
2. What has already been tried, and where does it fall short?
3. What gap remains?
4. What will our proposed approach do differently, and why might it work?

Ask who benefits and what measurable result would change their situation. Treat claims about prior work as unverified until sourced.

## APSET sections

### Area

- **Research work:** the research domain as a single label (e.g. TLS, privacy, blockchain)
- **Non-research work:** scope/context as a single label (e.g. billing, onboarding, harness)

**Length:** one word.

### Problem

State the concrete limitation, who is affected, and why it matters. Address the closest known alternatives and remaining gap only as needed to make the problem credible; label unsourced prior-work assertions.

**Length:** 2–3 sentences.

### System

Describe **our proposed approach**: what it does and why it could solve the problem. This is not the prior-work section.

When security is relevant, articulate the attacker's goal, capabilities, knowledge/assumptions, and explicit scope/exclusions. Clarify actors, assets, and trust boundaries if needed to make those claims meaningful. Do not invent a threat model where the user has not supplied its premises; ask.

**Length:** 2–3 sentences on our system; a concise threat-model subsection when applicable.

### Evaluation

Describe how the approach will be or was tested: setting, baselines, measures, and criteria for success or failure. Distinguish **planned tests** from **observed results**; include findings only when supplied or verified. State untested claims as hypotheses.

**Length:** 2–3 sentences.

### Takeaway

The single supported conclusion, or—before results exist—the intended contribution as a hypothesis. Do not claim an unobserved result.

**Length:** one sentence.

## End artifact

When all sections are thorough, deliver the APSET document in this shape:

```md
## Area
[one word]

## Problem
[2–3 sentences]

## System
[2–3 sentences on our proposed approach]

### Threat model
[only when security is relevant — attacker goal, capabilities, knowledge/assumptions, scope/exclusions]

## Evaluation
[2–3 sentences on planned tests or actual evaluation, with observed results identified]

## Takeaway
[one supported conclusion or proposed contribution]
```

No file write. No git commit. No copy-paste handoff prompt for a new session.
After the APSET document, append the `apset` completion suggestions from
[skill connections](../../../docs/skill-connections.md).

## Non-goals

- Do not fetch or bundle external threat-model examples
- Do not write to Obsidian
- Do not continue into implementation after delivering APSET unless the user starts a new request
- Do not auto-trigger — only when the user explicitly requests an APSET

## Key principles

- **Context first** — use conversation and repo context to avoid redundant questions
- **Incremental clarity** — each answer should sharpen the picture; vague answers get follow-ups
- **Security when relevant** — threat model lives in System, not as a separate research step
- **Abstract-ready** — when the user wants an abstract, aim for one sentence each on area and problem, two or three on system, about two on evaluation, and one on takeaway; favor clarity over a rigid count
- **Precise prose** — explain importance without jargon for its own sake; replace vague claims like “efficient” or “robust” with measured quantities or explicit hypotheses
- **Be flexible** — go back and re-ask when something new contradicts an earlier answer
