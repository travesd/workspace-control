---
name: LLM classifier ground truth principles
description: Repo-agnostic principles for LLM classifier ground truth — corpus is authoritative, clientId is not an LLM input, tainted-template handling, social corpus matching rules.
type: project
originSessionId: b822048f-5ea0-4685-be40-ed454892fc03
---
Principles that govern LLM classifier ground truth in detection-platform-metal. These are stable and repo-agnostic — apply when reviewing classifier outputs, building ground truth, or validating expected files.

- **Corpus is the only source of truth** — never use general knowledge to vouch for entities. If it isn't in the corpus, it isn't verified.
- **clientId is NOT an LLM input** — the LLM outputs `safeDomain`; the downstream rule engine sets `clientId`. Don't conflate them in prompts, expected outputs, or evaluation.
- **Tainted data**: content-similarity classifiers false-match on Cloudflare/Vercel/GitHub templates — ignore those matches when judging classifier accuracy.
- **Typosquats with no content** → monitor if confusable with a protected brand. Don't push.
- **Social corpus matching**: exact URL/alias on the same platform only. A LinkedIn entry does not verify a Facebook account; a Twitter handle does not verify Instagram.
