---
name: jev-knowledge-check
description: On /jev-knowledge-check, assess whether explored evidence suffices for a reliable answer.
disable-model-invocation: true
---

# Jev Knowledge Check

Run only on explicit `/jev-knowledge-check` invocation, after exploring that question. The check assesses whether the supplied evidence is sufficient, not Jev's prior knowledge, the answering LLM's accuracy, or the truth of a source.

1. Explore the files, sources, and checks needed for the prompt. Use its supplied question, or the latest user question if none is supplied. Summarize only relevant evidence into this JSON state (arrays may be empty):
   ```json
   {"question":"user's question","findings":["specific finding tied to a source"],"sources":["file path, URL, or check and what it establishes"],"unresolved_gaps":["what remains unknown"]}
   ```
   Include contrary findings and material gaps. Do not send conversation history, raw documents, attachments, credentials, or unrelated private data. If the prompt or essential findings contain secrets or unrelated private data that cannot be safely omitted, keep the check local and treat it as unavailable. A check with no findings or sources is unavailable; do the exploration first.
2. Read the live [TypeSafe HTTP API](https://docs.typesafe.ai/api.md) and [Choice/confidence guidance](https://docs.typesafe.ai/confidence.md) before using the check. The bundled `check.py` accepts the JSON state on stdin and uses `jev-latest` and one Choice with `sufficient`, `insufficient`, and `uncertain` options. Pipe the JSON to `python3 check.py` from this skill directory; provide `TYPESAFE_API_KEY` from the existing environment/secret store. It returns `status`, `next_step`, and (when available) Jev's confidence, probabilities and model. Keep the key and state out of logs and stored artifacts. If live docs are unavailable, use the locally validated contract and mention the limitation.
3. Follow `next_step` (experimental policy, not a calibrated correctness estimate):
   - **`proceed`** — Only `sufficient` with confidence ≥0.90. Say **“Jev assesses the explored evidence as sufficient (not independent verification).”** Answer from the evidence. This never grants permission for actions that otherwise require approval.
   - **`verify`** — `sufficient` with confidence ≥0.60 and <0.90, `uncertain` at any confidence, or `unavailable`. Say **“Jev's evidence assessment is uncertain; this answer may be unreliable.”** (For unavailable: **“Jev could not assess the evidence; this answer may be unreliable.”**) Consult a relevant source or run a check before relying on the answer. If missing information is essential, ask for it instead. Give only what the evidence supports, and name any unresolved gap.
   - **`stop`** — `sufficient` with confidence <0.60, or `insufficient` at any confidence. Say **“Jev did not find the explored evidence sufficient for a reliable answer.”** Do not give an unsupported substantive answer or take an action based on it. Seek a trusted source or tool, ask for clarification when context is missing, or hand off to a human. If independent evidence resolves the question, answer from that evidence and cite it; otherwise state the next needed input.

The bands 0.60 and 0.90 are trial settings for representative questions and actual answers. Jev's confidence measures concentration of its Choice distribution, not evidence quality or factual correctness. Normal evidence, safety, and authorization rules still apply. Manual checks use the same behavior.
