---
name: llm-prompt-iteration-methodology
description: "How to iterate LLM classifier/judge prompts in this codebase — concept-first framing, trace-justified disambiguators, variance characterization before comparing versions"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 28c3594c-205d-4fc9-b9e5-54a5fdd9ae29
---

Methodology validated across the autohunt impersonation_check seam iteration (v0→v8) in PR #64 (merged 2026-05-15). Apply when iterating any LLM judge/classifier prompt (content_judge, impersonation_check, domain_judge, page_type, social judges, d2_analysis, etc.).

**Rule 1 — Concept-first, not manifestation-enumeration.** Do not enumerate "how X manifests" (lists of patterns/shapes the model should match). Closed lists patch the visible failure subset, bias the prompt toward it, and harm generalization to unseen variants. Instead: trust the model's pre-trained concept, scope the question (which input, which target), and constrain the output schema. The label is a routing token, not the question.

**Rule 2 — Disambiguators must be trace-justified, never speculative.** When the model misclassifies, capture its actual reasoning chain (TRACE=1 → `routingInfo.stepsExecuted`) and add ONE disambiguator that corrects the *specific observed reasoning failure*. Each of v8's six disambiguators maps to a real traced failure. Speculative "this might help" disambiguators were proposed and explicitly rejected by the user until trace data justified them.

**Why:** The user pushed hard on this — "we shouldn't need to teach it what impersonation is, rather rely on its observation"; "I am uncertain about your suggested targeted disambiguators" → demanded tracing the problem incidents first. Reasoning from traces (not from incident summaries or intuition) is the required discipline.

**Rule 3 — Single-shot eval numbers mislead on borderline cases; characterize variance before comparing versions.** gpt-5.4-nano on flex tier has real run-to-run variance at temp=0. A one-shot 70-sample scored 92.8% (a low draw); an 8-hard-cases × 5-iterations variance test showed the true mean ≈ 96%. Before declaring a prompt version better/worse, run the flaky/boundary cases N times. The realistic accuracy floor is the *mean*, not any single run.

**Rule 4 — Asymmetric input visibility is a valid lever.** Stages with different optimization targets should get different inputs. `page_title` helped the upstream catcher (content_judge: optimize recall) but, as a discrete input to the FP-filter seam, overpowered its "title alone doesn't decide" disambiguator and created FPs (optimize precision). Don't reflexively give every stage every input.

**How to apply:** New prompt version = new numbered yaml file (v_N+1), bump the `prompt_cache_key`, rewire the workflow signature. Keep a `seam-iteration-history.md`-style ledger in the task dir documenting what each version changed and the trace evidence that justified it. Validate against [[curated-70-sample-dataset]] (or the relevant ground-truth set); compare *means*, not single runs.

Relates to [[feedback-llm-for-intelligence-not-lookup]] (LLMs for novel-pattern reasoning, not lookups) and [[curated-70-sample-dataset]] (the regression benchmark).
