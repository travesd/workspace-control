# Memory Index — detection-platform-metal

Workspace conventions, paths, and execution rules live in `/workspace/AGENTS.md` (imported by `/workspace/CLAUDE.md`). This index links to memories that add learning beyond what's in those files.

## Quick reminders (full rules in AGENTS.md)
- Single repo: **detection-platform-metal** (Docker Swarm + Redis Streams). Default base: `main`.
- Agent on host, repo code in containers. No host `python3`/`go`/`npm`.
- Local-stack validation only. Read-only DB via `/workspace/tools/db/dbctl`.
- **NEVER auto-push** — always ask before `git push` / `gh pr create`. `gh` auth: `travesd` (HTTPS, scopes `gist`/`read:org`/`repo`).
- Worktree work under `detection-platform-metal.worktrees/<branch>/`; task artifacts in `-work/busy/<task>/`; data products in `/workspace/datasets/`.
- Archive: `/workspace/archive/` for old GKE platform reference; backward-compat symlinks keep old paths resolving during PR migration.

## Project context
- [Metal vs legacy environments](project_metal_environments.md) — both metal and legacy GKE staging/prod still serve traffic; distinguish via `classifiers.pipeline-*-new.env` (metal) vs unsuffixed (legacy).
- [Pattern Recognition framework](project_pattern_recognition_framework.md) — umbrella for signal-type matching against curated libraries (Issues #10, #15). Single-incident classifiers (CNN, ModernBERT) stay in `classifier_results`.
- [LLM classifier ground truth principles](project_llm_classifier_ground_truth.md) — corpus is authoritative; clientId is not an LLM input; tainted-template handling; social-corpus matching rules.
- [Monitor lifecycle scope](project_monitor_lifecycle_scope.md) — monitor judgement reserved for brand-confusable hostnames currently showing no content; content-bearing non-impersonation pages should be suspicious/safe, not monitor.
- [Curated 70-sample dataset](project_curated_70_sample_dataset.md) — 50 impersonation + 20 non-impersonation ground-truth labels across 14+ brands for impersonation_check seam regression testing. Lives at `corpus-edits/filter/curated-70sample/final_dataset_50imp_20noimp.csv`.

## Reasoning discipline
- [Verify before asserting](feedback_verify_before_asserting.md) — never claim code/data/system behavior without verifying. Sub-agent reports are inputs, not facts. Includes 7 past incidents.
- [Read canonical scripts before asking scope](feedback_read_scripts_before_asking.md) — grep for `migrate*.sh`/`backup*.sh`/`sync*.sh`/`restore*.sh` and read them before asking the user what counts as "all X". Mirror the script's structure when proposing the work.
- [Workspace hygiene](feedback_workspace_hygiene.md) — create `busy/<task>/` BEFORE any artifacts.
- [Proposals not implementation](feedback_proposals_not_implementation.md) — propose, don't enter plan mode.
- [Log investigation incrementally](feedback_log_investigation_incrementally.md) — write findings to disk as you read, not at the end.
- [Archive-first read when porting](feedback_archive_first_read.md) — read the archived reference impl BEFORE writing new code.

## Sandbox environment
- [ARG_MAX — large argv unsafe >~128 KB](feedback_arg_max_argv_unsafe.md) — use tempfile/stdin for big curl/jq/python args.
- [Playwright headless](feedback_playwright_headless.md) — `.mcp.json` must keep `--headless` (no X server in sandbox).
- [filter-service Tranco bypass](feedback_filter_service_tranco_bypass.md) — when a fresh local stack's filter-service restart-loops with "unzip: context deadline exceeded", point `TRANCO_*_URL` env vars at `http://127.0.0.255:1/` via an extra Compose override.
- [virtiofs ENFILE — historical](feedback_virtiofs_enfile_workaround.md) — superseded 2026-04-24; `/workspace` is now ext4. No active rule.

## LLM prompt work
- [LLM prompt iteration methodology](feedback_llm_prompt_iteration_methodology.md) — concept-first not manifestation-lists; trace-justify every disambiguator; characterize variance before comparing versions; asymmetric input visibility is valid.

## Codebase-specific
- [atlas.sum auto-regenerated](feedback_atlas_sum.md) — don't flag as blocker on new migrations.
- [Cluster brand is human/LLM assigned](feedback_cluster_library_brands.md) — never derived from ASN/composition.
- [SSDeep block-size-96 unreliable](feedback_ssdeep_block_size_96.md) — set match_threshold ≥ 0.85; prefer DOM hashes.
- [SSDeep promote client-only](feedback_ssdeep_promote_client_only.md) — only promote clusters where brand matches an active client domain.
- [SSDeep classifier refresh](feedback_ssdeep_classifier_refresh.md) — selective refresh doesn't PubSub; needs service restart.
- [LLM for intelligence not lookup](feedback_llm_for_intelligence_not_lookup.md) — LLMs for novel-pattern reasoning; lookups/matrices belong in code.
- [Classification review](feedback_classification_review.md) — procedural rules for `/review-classification` skill.
- [Use e.code not e.key](feedback_ekey_vs_ecode.md) — Playwright synthetic events hide this.

## Git workflow
- [PRs target main in metal](feedback_pr_default_base_main.md) — pass `--base main` explicitly.
- [Never override commit identity](feedback_git_commit_identity.md) — always use `git config` (travesd noreply); no `--author=`, no `GIT_AUTHOR_*` env, no `git -c user.email=`. The real email belongs to a second GH account (`pfmailyer`) and breaks PR attribution.

## Archived (in `/workspace/archive/tooling-notes/memory-gke/`, not auto-loaded)
Topic files: `architecture`, `browser-pool-investigation`, `build-push`, `pubsub-monitoring`, `resource-contention`, `staging-env`, `mason-sonar-local-dev`, `testing-data`, `detection-data-v2-status`, `investigation-findings`. Feedback: `feedback_promote_is_argocd`, `feedback_monitor_skill_prod`, `feedback_never_submit_production`, `feedback_pr_default_base_develop`.

**Re-investigate before citing**: `browser-pool-investigation` and `resource-contention` reference Go code (browser.service.go, dom-info.service.go, sequential-enrichment.service.go) that likely lives in metal too. Bugs may still be real, operational framing is GKE-specific. Read current metal source before asserting findings as current.
- [Audit must mirror production definition](feedback_audit_mirror_production_definition.md) — auditor verdict = the component's OWN definition; handoff≠miss; scrub official-corpus.
