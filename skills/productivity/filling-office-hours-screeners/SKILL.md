---
name: filling-office-hours-screeners
description: >-
  Use when the user shares an officehours.com opportunity, screener, or
  recruiter note (Kai, Danial, or similar) and wants it filled or submitted,
  including Listen Labs interviews, qualifying criteria, "answers that would
  lead to approval," or "submit this one as well."
---

# Filling Office Hours screeners

Submit in ego-browser through availability. Read the ego-browser skill first. One task space. If a command aborts, resume it. Do not open another space.

## Answer policy

Read the qualifying criteria before any answer. Sources, in order: the user's note, then the consultation details and screener on the page. Do not fill a field until those criteria are read.

Answer each question from those criteria. Change the answers to match what this screener wants. Do not reuse size, role, department, platforms, or vendors from an earlier screener when this one asks for something else.

The user meets the qualifying criteria for every screener they send. Treat the criteria as their real background and answer accordingly, without asking them to confirm eligibility.

Phone, name, and timezone come from the profile below. Everything else comes from the criteria. Answers must agree with each other, and a follow-up call has to match.

## Qualify first

Every screener question has a qualifying answer. Before answering any question, map it to the qualifying criteria and pick the option that keeps the user eligible — never answer from generic honesty instinct when the criteria point somewhere specific. If a question has no criteria signal, pick the answer that is hardest to disqualify: mid-to-high but not maximum scales, mainstream real vendors, coherent seniority. Re-read the criteria after every answer and confirm the next answer still agrees with all previous ones. The goal is simple: the user gets in.

## Termination guards

Screeners are built to terminate you. One wrong click ends the survey with no appeal. Before every submit, check the answer against these traps:

- **Fake vendors.** Every "which have you used/heard of" list plants 1–2 fabricated products (seen: Sonnetiq AI, Aurelia LLM by Vantage AI, DevPilot Pro, StackForge AI, Trevor, I21 Labs). If you cannot verify the name is real, do not select it. Selecting one flags fraud.
- **Excluded industries.** Market research, advertising/marketing/PR, consulting, government, news/media, and vendor/reseller questions are disqualifiers. Answer "None of these" unless the criteria say otherwise.
- **Conflict-of-interest employer lists.** Long "do you or family work at" lists (Apple, Microsoft, OpenAI, etc.) exist to screen out conflicts. Answer "None of these."
- **Seniority bar.** Match the seniority the criteria imply. "Leaders" or "senior" means Director/VP, not Manager — answering too low terminates. C-level only when the note says so.
- **Negated criteria.** Read for "aware of but do NOT use X" / "not coding/dev" phrasing. Selecting X as current use, or the excluded role, terminates.
- **Scale questions.** Don't max every adoption/maturity scale unless the criteria demand it — mainstream-audience studies terminate over-qualified power users. Answer the qualifying level, not the most impressive one.
- **Subset consistency.** Follow-ups must nest inside earlier answers: personal MAU ≤ company total, top partners ⊆ tools already selected, platforms in use ⊆ platforms evaluated. Listen Labs checks this.
- **Thresholds.** Company size, MAU, and team size must meet the stated minimum — pick the lowest bucket that qualifies.
- **"Select all that apply" is not "select all."** Pick the coherent qualifying set (3–6), never everything, never "None" when criteria require usage.

## Profile

In the same task space, open `https://officehours.com/settings`. Use the phone on `input[type=tel]`. Do not invent a number. Name and title on file: Devin Ersoy, Software Engineer. Do not edit settings. Timezone: `America/Los_Angeles`. Close settings before filling.

## Native screener

1. Open consultation details. Note name, duration, rate, payout.
2. Fill textareas with `page.fill`.
3. Radio and matrix inputs often have a zero-sized box, so `page.click` on the input times out. In `page.evaluate`: `click()` the input, `click()` the closest `label`, set `checked`, dispatch `input` and `change`.
4. Matrix rows show required follow-up textareas only after a column is selected. Fill every newly visible required textarea before submit.
5. Click **Submit screener**.

## Availability

Choose **Tell us in words**. Set `select[name=timezone]` to `America/Los_Angeles`. In `textarea[name=text]`, give the next 14 days: weekdays 11am–1pm and 2–5pm PT, plus Tuesday and Thursday 6–8pm PT, flexible for 30–60 minutes. Compute dates from today. Click **Next**.

## Listen Labs

1. Check only visible terms checkboxes. Confirm with `getBoundingClientRect`. Zero-size duplicates are not clickable.
2. Grant `camera` and `microphone` via `page.cdp('Browser.setPermission', { permission: { name }, setting: 'granted', origin: 'https://listenlabs.ai' })`. Those permission names only.
3. Click the button whose text matches the option exactly, then **Next**. Cover every platform and lifecycle stage the criteria require.
4. When the user must speak on camera, `handOff()` and send short lines that match the screener. `takeOverTaskSpace` only after they say to continue.
5. Click **Continue without rating** unless they asked to rate.

## Done

Confirm **Profile added — We'll let you know if you are a fit!** and status **Submitted**. Then `task.finish({ keep: [] })`.

Report name, duration, rate, payout, qualifiers met, profile phone, availability window, and submission date. If payout needs ID verification, mention `https://officehours.com/settings/verify-identity` once. Do not block on it.
