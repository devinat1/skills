---
name: dissenter
description: >
  Stress-test a choice with an independent LLM view and Jev judgment (Choice,
  Score, or Noul). Use before giving user-facing advice, recommending, or
  evaluating a choice when two plausible courses exist, including low-stakes
  choices; skip routine execution, factual lookups, and status questions.
  Explicit /dissenter requests can also evaluate factual questions.
---

# Dissenter

Stress-test a choice without manufacturing a debate. The invoking LLM translates
one question into a Jev primitive; Jev supplies the judgment and probabilities.
Keep the Original view independent. Jev may agree.

## Advice gate

This is the authoritative gate for every owned skill that gives user-facing advice.

Apply this gate after gathering relevant context and before recommending,
prioritizing, selecting, scheduling, or proposing a course of action for the user.
Low-stakes choices qualify when two credible answers exist. Factual reporting,
a procedure the user already chose, routine execution, and immediate safety
instructions do not. Explicit `/dissenter` requests may also ask factual questions.

When the gate applies, invoke `dissenter` with the decision, user's goal, and
relevant evidence. Present both views without selecting a winner or default.
End with one question asking the user to choose or supply another option; wait
before taking an action that depends on the choice. This gate overrides local
instructions to choose or advance automatically.

## Run

1. For automatic invocation, apply the **Advice gate**; otherwise answer normally.
   Explicit `/dissenter` requests may also ask factual questions. Gather the user's
   exact question, goal, and relevant evidence. Separate facts, sources, missing
   information, and assumptions. The LLM chooses the best format
   below and continues without asking the user to select or approve a format.
   Resolve ambiguity with the smallest reasonable assumption and state it,
   including the time period or meaning of vague terms when needed. Missing
   evidence stays missing; an assumption is not a discovered fact.
2. Rewrite the question using **Choose the primitive**. Preserve its subject,
   requested judgment, scope, and polarity. Before calling Jev, show the type,
   exact rewritten question, criteria, and assumptions. This is disclosure,
   not an approval stop. Check that an answer to this rewrite would answer the
   user's original question—not a nearby question about assessment methods,
   evidence quality, or whether a dissent deserves consideration.
3. Launch one independent **Original** subagent with the exact user question,
   shared evidence, and disclosed assumptions. Ask for direct analysis, assumptions,
   and tradeoffs without choosing for the user. Do not send it Jev's result or
   feed its answer into Jev's state. Follow the harness's delegation protocol;
   collect its result before reporting. If unavailable, label the Original view
   unavailable rather than substituting the coordinator's answer.
4. Check `TYPESAFE_API_KEY` without printing it. Load it from an already configured
   local secret store if available; never include keys in chat, files, or logs.
   Read the [TypeSafe index](https://docs.typesafe.ai/llms.txt),
   [HTTP API](https://docs.typesafe.ai/api.md), and chosen primitive's page below.
   Use the live contract; if docs are unavailable, disclose that and use a verified
   local contract or mark Jev unavailable. Send one question as described in
   **Request**. Missing key or failed call follows **Unavailable**.
5. Validate and render the returned answer according to its type. Compare the two
   views on the same question. Preserve agreement and uncertainty; do not manufacture
   an opposing view or add reasoning that Jev did not produce.

## Choose the primitive

Choose by what the answer means, not just its opening word. For a compound request,
choose the main judgment and disclose what is not covered instead of silently
bundling unrelated dimensions. For an open-ended request, state the bounded
interpretation and any LLM-proposed candidates; Jev cannot generate prose or
select a candidate that was not supplied.

| Answer needed | Primitive | Criteria | Returned fields |
| --- | --- | --- | --- |
| One of a defined set of options | [Choice](https://docs.typesafe.ai/primitives/choice.md) | Map of option IDs to complete, distinct descriptions | `choice`, `probabilities`, `confidence` |
| Degree on one ordered dimension | [Score](https://docs.typesafe.ai/primitives/score.md) | 2–10 ordered, concrete level descriptions | `score`, `legend`, `probabilities`, `confidence` |
| Whether a proposition is true | [Noul](https://docs.typesafe.ai/primitives/noul.md) | Optional `true`/`false` definitions of the proposition and its negation | `noul` |

- **Choice:** Include every user-supplied option. When generating candidates, label
  them as LLM-proposed, include the original course if one exists, and include
  `none_fit` when no listed option may apply. Do not limit the set to dissenting
  alternatives. The distribution compares these options, not every possible answer.
- **Score:** Define each level independently with an observable situation, not
  merely "low / medium / high" or a number. Keep one dimension. For N levels,
  the continuous score spans 0 to N−1; it is not a probability or a percentage.
- **Noul:** A high value means the stated proposition is true. Its negation is
  not "no supporting evidence"; lack of evidence does not establish falsehood.
  Evaluate evidence support only when the user actually asks about evidence support.
  There is no separate confidence field. A value near 0.5 is uncertainty, not
  medium intensity.

Example question objects (adapt one; do not send all three):

```json
{
  "type": "choice",
  "instructions": "Which listed database best meets the application's stated requirements?",
  "criteria": {
    "sqlite": "Use SQLite as the application database.",
    "postgres": "Use PostgreSQL as the application database.",
    "none_fit": "Neither database meets the stated requirements."
  }
}
```

```json
{
  "type": "score",
  "instructions": "How severe is the reported bug's effect on the user's workflow?",
  "criteria": [
    "Cosmetic defect; the user can complete the workflow normally.",
    "The workflow is impaired, but a usable workaround exists.",
    "The workflow is blocked and no usable workaround exists."
  ]
}
```

```json
{
  "type": "noul",
  "instructions": "Does the proposed migration require application downtime?",
  "criteria": {
    "true": "Completing the migration requires a period of application unavailability.",
    "false": "The migration can complete while the application remains available."
  }
}
```

## Request

Prepare valid JSON in a temporary `request.json`, using a JSON serializer so user
text is escaped safely. Set `model` to `jev-latest`, `state` to an object containing
`user_question`, `goal`, `evidence`, `assumptions`, and any relevant options or
context. Set `questions` to `{"answer": <chosen question object>}`. Fill every
placeholder. All question meaning must be in `instructions`/`criteria`: question
IDs are not sent to the model. Send only relevant context authorized for TypeSafe,
not credentials or unrelated private material. Disable shell tracing.

```bash
: "${TYPESAFE_API_KEY:?TYPESAFE_API_KEY is required}"
curl --silent --show-error --fail-with-body --max-time 60 \
  https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @request.json
```

Read `answers.answer`. Verify the returned type matches the request, required
fields exist, and numeric values are finite and in range. Choice/Score distributions
must contain exactly the supplied options/levels and sum to approximately 1;
Choice's selection must be an allowed option. Score's legend must match the levels
and its value must be in 0..N−1. Treat malformed results as unavailable.

## Return

Use these headings, adapting fields to the selected primitive:

```markdown
## Original view
[Independent subagent's direct answer, assumptions, and tradeoffs—or unavailable]

## Jev view
- **Format and question:** [primitive and exact question sent]
- **Criteria and assumptions:** [options, ordered levels, or proposition definition; scope]
- **Result:** [Choice: selected option; Score: continuous value and scale; Noul: P(proposition true)]
- **Distribution and confidence:** [Choice/Score only: all probabilities and confidence]
- **Limits:** [evidence gaps, sources, and returned model name]

## Takeaways
[Agreement or disagreement about the actual question; label any LLM interpretation]

## Your decision
[For a decision: ask the user to choose; for a factual question: give the bounded conclusion]
```

Round displayed probabilities/confidence to whole percentages; retain raw values
when checking them. Attribute them to Jev conditioned on this question, criteria,
and supplied state—not verified real-world frequencies. Confidence measures
concentration of the distribution, not correctness. Do not invent a confidence
value for Noul or an explanation from Jev. Do not select a course for the user or
act on a consequential choice without their decision.

## Unavailable

If the key is missing, the request fails, or the response is invalid, write
`Unavailable: [brief sanitized reason]` under **Jev view**. Keep the completed
Original view and only supported takeaways. Do not fabricate probabilities or
use an LLM dissent fallback. If the Original view fails, the Jev result can still
be reported as a single available view, not as a completed two-view comparison.

For routing and template checks, see [TESTING.md](TESTING.md).
