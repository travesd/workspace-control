---
name: LLM workflows add intelligence, not execute lookup tables
description: Detection-platform governing principle — use LLMs only for content understanding, multimodal reasoning, novel-pattern detection; move lookup tables, string matching, and policy matrices to code even when they currently live in a prompt
type: feedback
originSessionId: a9d4383d-0f97-4c25-927b-d1cb1f8fb877
---
**Rule:** In detection-platform LLM workflows, use LLMs for the things code can't do well — content understanding, multimodal reasoning, novel-pattern detection, ambiguity handling. Use code for lookup tables, string matching, suffix classification, edit distance, policy matrices, and deterministic rules — even when those currently live inside a prompt.

**Why:** User stated this explicitly during the llm-judge-domain-workflows review (2026-04-10): "the point of our workflows is to add intelligence to cover things we can't do with ML models." The current d2_analysis_v4 violates this principle in several places:
- `domain_brand_extract` uses an LLM to apply a hardcoded list of business-vs-generic suffixes — the list is literally pasted into the prompt.
- `domain_typosquat_match_v2` uses an LLM to execute a 6×3 page_category × nameUniqueness verdict matrix — the matrix is a lookup table written in natural language.
- The threat judge has a 5-step decision tree encoded as prompt rules that could be a switch statement.

Using LLMs for these tasks adds sampling variance (same input can flip verdicts), latency, cost, and debugging pain (no breakpoints, no unit tests), and sometimes reduces accuracy because the LLM goes off-script.

**How to apply:**
- When reviewing or designing an LLM workflow step, ask: "Does this prompt contain hardcoded lists, rule matrices, threshold tables, or decision trees?" If yes, those belong in code.
- Keep the LLM in the loop for: reading page content, inferring brand portrayal/framing, detecting industry mismatch, recognizing novel patterns, multimodal reasoning, genuinely ambiguous judgment calls.
- When moving a rule from prompt to code, output "unclear" / "needs_review" on edge cases the code rule can't confidently handle, and let an LLM arbitrator pick up only those. Hybrid, not replacement.
- This principle does NOT touch ML classifier accuracy — ML upstream stays as-is. The redesign is about the LLM-land middle layer, not the ML-land layer.
