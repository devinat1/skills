---
name: novelty-search
description: Refine research questions with Jev for up to ten rounds, then check high-probability candidates on Consensus.
disable-model-invocation: true
---

# Novelty search

Generate research questions, screen them with Jev, and send only qualifying candidates to Consensus through Ego. Find a potentially new research contribution, not merely a different benchmark. Keep this separate from `research-gap`. Neither model's judgment proves novelty.

## 1. Fix the idea and evidence

Use the user's stated idea or the latest substantive idea in chat. Write one sentence naming its population/setting, comparison or mechanism, and outcome. Ask one clarifying question only if an essential part is missing. Keep this anchor fixed unless the user approves a change. Assess the idea, not just limitations of its current implementation.

Prepare a minimized prior-work packet from supplied papers, existing research notes and accessible primary sources: source IDs/URLs, population, setting, inputs, method/comparator, outcome, contribution, and access limits. Separate verified source content from secondary summaries and unsupported claims. Jev does not search the literature; an empty packet cannot establish novelty. If no useful prior-work evidence exists, request it or obtain permission for a separate discovery pass before screening. Do not invent papers or source claims from Jev's answers.

## 2. Generate and approve a round

Draft up to five distinct, answerable questions. Change a substantive dimension, not just wording. Explain each question's connection to the anchor and its difference from earlier candidates. Show questions before external submission and get approval; standing approval for subsequent in-scope rounds is allowed if explicit. Explain that screening sends the minimized questions and evidence to TypeSafe, and only qualifying questions proceed to Consensus. Keep credentials and unrelated private material out of both services.

Use at most **10 rounds and 50 generated candidates total**, including rounds where none passes Jev. Resuming does not reset these counters. Keep a working ledger in conversation with stable candidate IDs, round, question, evidence version, Jev output, Consensus result, source check and disposition. Read [TESTING.md](TESTING.md) when changing this workflow.

## 3. Screen with Jev first

Read the installed `typesafe-ai` skill and its live index, Choice, confidence and current API documentation before calling Jev. Use the documented API/SDK with available credentials; missing access is a blocker, not permission to invent scores or bypass this stage.

For each candidate, ask one **Choice** question, batching independent questions over the same evidence state. Reference the candidate explicitly in the instructions; question IDs are not visible to the model. Use this judgment:

> Relative to the supplied prior-work evidence, does this research question propose a substantive unanswered contribution, rather than a restatement or an arbitrary benchmark variation? Judge only the evidence available; select unclear when it cannot support the comparison.

Use these criteria:

- `potentially_novel`: The evidence supports a meaningful unanswered claim within the anchor, distinguishable from the closest work on a substantive dimension.
- `already_addressed`: The closest work answers the same claim with matching scope and qualifications.
- `incremental_variant`: The difference is only wording, arbitrary setting restrictions, implementation, or benchmark configuration without a distinct research claim.
- `unclear`: Missing, weak or conflicting evidence prevents distinguishing the candidate from prior work.

**Default gate:** `choice == potentially_novel` AND `probabilities.potentially_novel >= 0.80` AND `confidence >= 0.80`. Validate response fields and probability ranges before using them. Record the returned model, full probabilities, confidence and usage. Invalid responses are errors, not rejected candidates.

The thresholds are adjustable starting policy, not calibrated novelty guarantees. Probability refers to this evidence-conditioned label; confidence describes concentration of the distribution. A confident rejection never qualifies. Disclose thresholds before the first call and hold them fixed for the run unless the user explicitly changes them. Preserve initial results; do not retry unchanged questions, remove counterevidence, or lower thresholds merely to get a pass. Jev returns judgments, not explanations: ground revisions in source evidence, not invented Jev reasoning.

If none qualifies, refine substantive questions from known overlaps and limitations and return to step 2. If any qualify, show their exact wording, probabilities and confidence before step 4; obtain approval if existing approval did not cover Consensus submission. Jev passing alone never completes the search.

## 4. Check qualifying questions on Consensus

Read `ego-browser`, create one TaskSpace for the whole Consensus phase, and reuse it across rounds. Open `https://consensus.app/` only after at least one candidate passes the Jev gate. Submit qualifying approved questions individually, highest novelty probability first, until a supported candidate is found. Keep unsubmitted candidates marked as such.

Ask neutrally: “Has published research already answered this question? Cite the closest papers, explain their overlap and differences, and assess whether this is a potentially novel research contribution or merely a different benchmark. State uncertainty and evidence gaps.” Do not tell Consensus that Jev rated it highly or ask it to confirm novelty. Observe each completed answer; record its result URL, exact novelty wording or a short quote, citations and limitations. No results is *unclear*, not novel.

For a positive novelty claim, inspect the closest cited papers' abstracts or accessible primary text. Compare population, setting, inputs, method/comparator, outcome and contribution. Mark directly overlapping claims **contradicted**, inaccessible or ambiguous comparisons **unverified**, and an evidence-supported distinction **provisionally distinct**. A broad “more research needed” statement alone does not establish a new contribution.

Stop successfully only when Consensus explicitly identifies a potentially novel question and the closest-source check supports the distinction. Otherwise check remaining qualifying candidates, incorporate verified new evidence into the packet, and return to step 2 if rounds remain. Maintain separate Jev and Consensus judgments when they disagree. Never silently substitute another service for Consensus. For access failures, login, rate limits or user takeover, follow Ego's stop/handoff rules and preserve progress; follow its finish rules on completion.

## 5. Report the bounded result

Stop at the first supported candidate or after ten rounds, whichever occurs first. A user stop or service blocker is not search exhaustion. Report the anchor, thresholds, round/candidate counts, Jev-screened versus Consensus-submitted counts, and the ledger's dispositions. For a candidate give the exact question, Jev probabilities/confidence, Consensus wording and result link, closest prior work with specific overlap/difference, and source-check limitations.

If exhausted, say **“No supported candidate found in ten rounds”**, distinguishing no Jev qualifiers from qualifiers rejected or left unverified by Consensus/source checks. This does not mean the idea is not novel. Adaptive screening can favor false positives; disclose that the selected candidate came from an iterative search and requires broader literature review. Save no searches to repo files or memory unless asked.
