# Workspace Knowledge Source Migration Plan

Date: 2026-05-25
Status: implemented in repo; workspace-level note copies created under
`/workspace/detection-platform-metal-work/knowledge/`

## Objective

Move non-operating-model knowledge out of `/workspace/workspace-control` without
deleting it.

`workspace-control` should remain the versioned source for workspace operating
model, agent workflow, shared skills, activation rules, and harness
configuration. Product, release, incident, dataset, service, and task-specific
facts should have a workspace/product source of truth outside this repo.

## Current Problem

The first knowledge seed imported provider-local memory into
`/workspace/workspace-control/knowledge/`. That made useful notes available to
Claude and Codex, but it also mixed three classes of knowledge:

- workspace-control operating-model rules,
- broader workspace operating facts,
- detection-platform-metal product/service facts.

After the repo scope was tightened in `b7c6863 docs(knowledge): clarify
workspace-control scope`, the third class should not stay canonical in this
repo. The correct action is migration, not deletion.

## Proposed Source-Of-Truth Split

| Knowledge Type | Canonical Home | Examples |
|---|---|---|
| Workspace-control operating model | `/workspace/workspace-control/knowledge/`, docs, ADRs, shared skills | repo-first activation, task resumability, instruction-thinning, skill maintenance |
| Workspace operational facts used by agents | `/workspace/detection-platform-metal-work/knowledge/` | local-stack gotchas, environment distinctions, workspace-specific review conventions |
| Product behavior or release facts | product repo docs, task summaries, or product issue/PR docs | release-note generation behavior, classifier semantics, service internals |
| Dataset-specific facts | `/workspace/datasets/<dataset>/MANIFEST.*` and dataset docs | curated corpus contents, labels, evaluation scope |
| Task-specific findings | task `notes.md` / `SUMMARY.md` | one-off incident findings, PR review conclusions, local command output |

## Candidate Classification

Keep in `/workspace/workspace-control/knowledge/`:

- `workspace-organization-efficiency-20260520.md`
- `feedback_git_commit_identity.md`
- `feedback_verify_before_asserting.md`
- `feedback_workspace_hygiene.md`
- `feedback_log_investigation_incrementally.md`
- `feedback_proposals_not_implementation.md`
- `feedback_read_scripts_before_asking.md`
- `feedback_arg_max_argv_unsafe.md`
- `feedback_archive_first_read.md`
- `feedback_pr_default_base_main.md`

Likely move to workspace-level knowledge after verification:

- `project_metal_environments.md`
- `feedback_filter_service_tranco_bypass.md`
- `feedback_playwright_headless.md`
- `feedback_atlas_sum.md`
- `feedback_ekey_vs_ecode.md`

Likely move to product repo docs, product task summaries, or product-specific
workspace knowledge after verification:

- `feedback_audit_mirror_production_definition.md`
- `feedback_classification_review.md`
- `feedback_cluster_library_brands.md`
- `feedback_llm_for_intelligence_not_lookup.md`
- `feedback_llm_prompt_iteration_methodology.md`
- `feedback_ssdeep_block_size_96.md`
- `feedback_ssdeep_classifier_refresh.md`
- `feedback_ssdeep_promote_client_only.md`
- `project_llm_classifier_ground_truth.md`
- `project_monitor_lifecycle_scope.md`
- `project_pattern_recognition_framework.md`

Move to dataset manifest or dataset documentation after verification:

- `project_curated_70_sample_dataset.md`

Do not move any note until its destination exists and the source task, dataset,
or product documentation path is recorded.

## Migration Steps

1. Create the workspace-level knowledge home:

   ```text
   /workspace/detection-platform-metal-work/knowledge/
   ```

   Include:

   - `README.md` defining scope,
   - `TEMPLATE.md`,
   - generated `INDEX.md`,
   - generated `index.json`.

2. Extend or parameterize `knowledgectl` so agents can search:

   - workspace-control operating-model knowledge,
   - workspace-level detection-platform-metal knowledge,
   - optionally both with a `--scope all` or equivalent mode.

   Do not make agents load either tree at session start. Search first, then
   open specific notes.

3. Classify each legacy note using the table above.

   For each note, record:

   - current file,
   - destination,
   - reason,
   - source evidence,
   - whether the fact was freshly verified or preserved as historical memory,
   - replacement pointer left behind, if any.

4. Move notes by preserving provenance.

   Use `git mv` inside `/workspace/workspace-control` only for notes that stay
   in that repo. For notes moving outside the repo, copy to the new workspace
   knowledge home with the original source, verified date, and migration
   metadata intact, then remove from `workspace-control` in the same reviewed
   commit.

5. Leave redirects for one transition cycle.

   For moved notes, either:

   - leave a short pointer file in `workspace-control/knowledge/` marked
     `status: superseded`, or
   - update all known references and include a migration manifest.

   Prefer pointer files when references are likely to exist in older task
   summaries or provider memory.

6. Update skills and docs.

   Review at least:

   - `durable-learning-capture`,
   - `research-to-knowledge`,
   - `workspace-status`,
   - `agents-md-review`,
   - `/workspace/AGENTS.md` references to knowledge lookup.

   The final instructions should make the split clear:

   - workspace-control knowledge for operating model,
   - workspace-level knowledge for detection-platform-metal agent facts,
   - product/dataset/task homes for narrower facts.

7. Validate.

   Run:

   ```bash
   cd /workspace/workspace-control
   ./tools/check-sensitive-content .
   ./tools/knowledgectl lint
   ./tools/knowledgectl index --check
   ./tools/renderctl dry-run --mode all
   ./tools/renderctl dry-run --mode live-check
   git diff --check
   ```

   Also run the workspace-level knowledge lint/index command once that tooling
   exists.

8. Activate only the lookup/instruction changes that need live behavior.

   Moving files inside task/knowledge homes does not by itself require live
   provider mirror sync. If `/workspace/AGENTS.md`, shared skills, or live tools
   change, use the repo-first activation process with rollback notes.

## Non-Goals

- Do not delete legacy knowledge.
- Do not silently drop weak-provenance notes.
- Do not move product facts into `workspace-control` to keep one searchable
  tree.
- Do not make provider-local memory authoritative.
- Do not activate Pi or change Pi draft files.
- Do not edit product repo docs until a product-doc destination is deliberately
  selected.

## Implementation Notes

- Workspace-level knowledge home selected:
  `/workspace/detection-platform-metal-work/knowledge/`.
- Moved notes leave superseded pointer files in
  `/workspace/workspace-control/knowledge/` for one transition cycle.
- Product-specific notes were preserved as workspace-level knowledge with
  `status: under-review` until a deliberate product-doc destination is chosen.
- Dataset note preservation points at
  `/workspace/datasets/curated-impersonation-70sample/MANIFEST.json` as the
  canonical dataset fact source.
- `tools/knowledgectl` supports `KNOWLEDGE_DIR=/path/to/knowledge` for
  linting, indexing, stale checks, and search across the selected tree.

## Resolved Questions

- Workspace-level knowledge lives at
  `/workspace/detection-platform-metal-work/knowledge/`, keeping it scoped to
  this sandbox.
- Moved notes leave pointer files because older task summaries and provider
  memory may still reference the old paths.
- Product-specific notes first move to workspace-level knowledge and remain
  under review. Product-doc promotion is a separate decision.

## Recommendation

Use `/workspace/detection-platform-metal-work/knowledge/` as the workspace-level
home and migrate in two slices:

1. Move obvious product/dataset notes out of `workspace-control` with pointer
   files and a migration manifest.
2. Update `knowledgectl` and shared skills so agents can search the correct
   source by scope.

This preserves all knowledge while making `workspace-control` a cleaner control
repo rather than a general product memory store.
