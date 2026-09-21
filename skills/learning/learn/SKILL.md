---
name: learn
description: Route a conversation, path, URL, file, or topic to one focused learning modality. Use when the user wants to learn but has not chosen between a Socratic lesson, interactive illustration, coding lab, or exam. It identifies and confirms the topic, recommends a modality, and hands off without teaching or grading.
---

# Learn

Act as the learning router. Topic selection and modality handoff are the whole
job.

## Choose the topic

Read [learning context](../learning-context.md). Resolve the current conversation
plus any argument and recall relevant agent memory.

Infer a short list of plausible learning topics from user-authored context and
the supplied sources. Keep the list to the fewest distinct topics that explain
the request:

- If one topic is plausible, state it in one line and ask the user to confirm.
- If several are plausible, show the short list and ask the user to choose
  exactly one.
- If none has enough support, ask the user what they want to learn.

Ask one question per turn. Do not infer a knowledge gap from silence or from an
assistant-authored claim.

## Choose the modality

After topic confirmation, present all four choices with equal visual weight and
mark one as `Recommended`:

- `/socratic-teacher` — guided understanding through explanation and
  explain-back.
- `/illustrate` — an interactive map of relationships, terminology, and flow.
- `/lab` — an executable coding exercise with unit tests.
- `/exam` — a complete knowledge test with a separate answer key.

Recommend by the dominant need:

- incomplete understanding or guided reasoning → `/socratic-teacher`
- relationships, flow, terminology, or structure → `/illustrate`
- executable implementation practice → `/lab`
- measurement of existing knowledge → `/exam`

Ask the user to choose. Do not choose on their behalf.

## Hand off

Build the concise learning brief defined in
[learning context](../learning-context.md). Say which selected skill is being
used and why, then invoke it with the brief.

The selected modality owns the workflow and its completion suggestions from
this point. `/learn` does not teach, assess knowledge, grade, create artifacts,
or write knowledge claims to memory.

## Automatic Jev check

When the topic is confirmed but the modality is not explicitly chosen, first form the ordinary recommendation, then send the compact learning brief (stable source IDs) after reading the existing `typesafe-ai` skill and its current API documentation. Only do this with operator authorization to disclose minimized evidence to TypeSafe; remove credentials and unrelated private data, and retain the ordinary workflow when consent or access is unavailable. Ask a Choice among `socratic-teacher`, `illustrate`, `lab`, `exam`, and `unclear`; each option must use the modality definitions in this skill, and `unclear` means the brief does not distinguish a dominant need.

Use it only to check the marked recommendation; present all four choices and let the user choose. On ambiguity, unavailability, or disagreement, use the existing dominant-need rules and confirmation flow.
