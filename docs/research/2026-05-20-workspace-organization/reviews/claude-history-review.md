# Claude History Review

Date: 2026-05-20
Reviewer: Claude (Opus 4.7, 1M context, session `60dffdd9`)
Scope: workspace artifacts, recent Claude transcripts, Claude provider-local memory, the prior `/insights` report output, and the available Claude skill set. No transcript quotes long enough to leak prompts or secrets; evidence given as paths and counts.

## `/insights` Availability

**`/insights` is NOT currently available in this Claude session.**

- Not in the system-reminder skill list for this session.
- Not in `/workspace/.claude/skills/`, `/home/user/.claude/skills/` (no such dir), `/home/user/.claude/commands/` (empty), or any installed plugin under `/home/user/.claude/plugins/cache/`.
- The Superpowers plugin v5.1.0 ships 14 skills (`finishing-a-development-branch`, `systematic-debugging`, `brainstorming`, ...); none is `insights`.
- `/home/user/.claude/history.jsonl` shows `/insights` was invoked 5 times across this workspace: 2026-03-30, 2026-04-14, and three times on 2026-05-19. Each run produced a static HTML report; the three most recent live at `/home/user/.claude/usage-data/report-2026-05-19-*.html`.

I used the most recent of those (`report-2026-05-19-171058.html`, generated 2026-05-19) as a substitute data source because it covers 774 messages across 50 sessions from 2026-04-16 → 2026-05-19 — a richer dataset than I could mine inside this turn. Findings below mark which evidence came from that report vs. live transcript/file scan.

## Evidence

### Workspace state (live scan, 2026-05-20)
- `busy/` task dirs: 26; resume files: 25; missing resume: `busy/autohunt-social-trace/` (matches `SESSIONS.md`).
- 9 of those resumes flagged by `sessionctl index` as non-standard or unparseable (e.g. `audit-pr64-before-after/resume.md` has a placeholder `(this session)` row that `sessionctl` cannot parse; `llm-detection-ui/resume.md` is the empty template).
- `SESSIONS.md` lists 11 live tmux agent panes with **no recorded session ID** (`0:1`..`0:12`) — exactly the recovery-blocker pattern.
- `done/INDEX.md` is healthy (16 closed tasks, 9 day dirs, each has `SUMMARY.md`).
- `investigations/` holds 11 dirs including this one and `session-recovery-20260512` — itself evidence that recovery is recurring work.

### Provider-local memory (Claude-only)
- `/home/user/.claude/projects/-workspace/memory/`: 28 markdown files + `MEMORY.md` index (540 lines total). Index is well curated: `feedback_*` (rules), `project_*` (current context), pointers to archived GKE memories.
- This store is loaded into every Claude session via the system reminder but is **not visible to Codex by workspace contract** (Codex would have to grep host paths). 11 user-message references to "memory" appeared in recent transcripts.
- Examples of high-value durable rules that only live here: `feedback_verify_before_asserting.md` (7 past incidents), `feedback_git_commit_identity.md`, `feedback_arg_max_argv_unsafe.md`, `feedback_pr_default_base_main.md`.

### Recent Claude transcripts (live scan)
- 73 .jsonl files under `/home/user/.claude/projects/-workspace/`, 735 MB total. Largest single transcript 32.5 MB (`28c3594c…` 2026-05-15) — that is a single Claude session.
- Sampled the 8 most recent sessions. Cross-session lookup counts (mentions in transcript blob, not all "fresh reads", but a useful proxy):

  | Lookup pattern              | Hits | Sessions (of 15) |
  |-----------------------------|-----:|-----------------:|
  | `AGENTS.md`                 |  758 |               11 |
  | `dbctl`                     |  548 |                8 |
  | `INDEX.md`                  |  391 |                7 |
  | `resume.md`                 |  340 |                9 |
  | `MEMORY.md`                 |  275 |                6 |
  | `accessctl`                 |  165 |                5 |
  | `CLAUDE.md`                 |  149 |               15 |
  | `ACTIVE.md`                 |   96 |                6 |
  | `gh pr view/list`           |   71 |               10 |
  | `SESSIONS.md`               |   53 |                7 |
  | `done/INDEX`                |   52 |                5 |
  | `archive/` lookups          |   49 |                8 |
  | `gatewayctl` / `sessionctl` |   65 |                7 |
  | `git worktree list`         |   20 |                5 |
  | `docker-swarm.env`          |   17 |                6 |

- Early-session pattern: in 5 of 6 sampled sessions, Claude's first 8 tool calls were the same scout sequence (`ls busy/`, `cat ACTIVE.md`, `gh pr view <N>`, `ls worktrees/`, grep for related closed tasks). This is the lookup tax.

### Friction signals from user messages (live scan, 15 sessions)
- "ultrathink": 128 instances across 10 sessions — i.e. the user routinely has to escalate me to think harder. The `/insights` report scored "Frustrated/Dissatisfied" at 30 of 194 satisfaction signals, dominated by "Buggy Code" (23) and "Wrong Approach" (23).
- Concrete recent corrections (this week):
  - `04f1660e` 2026-05-20: "AGENTS.md gotcha says the LLM judge benefits from the full-page screenshot — this is nonsense". A stale AGENTS.md claim caused an off-target plan.
  - `20c69ebd` 2026-05-20: "where did pfmailyer user come from? … who the fuck is changing who we commit as?" Commit-identity drift recurred even though it is the most recently saved feedback memory (`feedback_git_commit_identity.md`).
  - `39a54f02` 2026-05-20: "no thats not the only discriminator, it was an example :facepalm". Over-fit to a single example.

### From the 2026-05-19 `/insights` report (50-session aggregate)
- Code Review is the dominant workload (23/60 stated goals); 18 days, 43 msgs/day, 38 % multi-clauding overlap.
- Top friction categories (model-classified): Unverified Claims (multiple sessions), Scope Drift / Misread Instructions (multiple), Infrastructure Interruptions (usage-limit / OOM cutoffs on long autonomous runs).
- 119 "Command Failed" tool errors, 4 "File Too Large" — proxies for unfamiliar terrain and ARG_MAX-style boundaries.
- The report's own three CLAUDE.md additions overlap exactly with what's already in `MEMORY.md` (`feedback_verify_before_asserting.md`, `feedback_read_scripts_before_asking.md`, scope discipline) — i.e. the rules exist; the system reminder just isn't preventing the drift.

## Findings (ordered by impact)

### 1. Durable learnings are trapped in Claude-local memory; Codex can't see them by contract.

`MEMORY.md` is the highest-leverage knowledge surface in this workspace — 28 files of distilled rules — but it lives under `~/.claude/projects/-workspace/memory/` and is loaded only into Claude. Codex's review (line 21) flags the same gap from its side. Recent in-session corrections (commit identity, screenshot gotcha) show the rules exist *and* still get violated, so part of the fix is mirroring them into a provider-neutral store, and part is making them harder to ignore at decision time, not just at session start.

This is the single change with the broadest cross-agent payoff: every workspace learning becomes addressable from either provider.

### 2. Session-start scout sequence is the same in nearly every Claude session.

Claude reliably starts with: read `CLAUDE.md`/`AGENTS.md` (auto), then `ls busy/`, `cat ACTIVE.md`, `cat SESSIONS.md`, `gh pr view <N>`, `ls worktrees/`, then a task-specific grep. With 73 sessions × ~8 redundant scout calls × Bash latency, the lookup tax is real and predictable. A small `workspace-status` skill or a generated `STATUS.md` (joined from `sessionctl index` + `gh pr list` + `git worktree list` + gateway state) would cut this to one read. Codex's `workspace-artifact-inventory` proposal covers the same ground from the inventory direction.

### 3. Long-lived task dirs accumulate state that should have been harvested.

The `/insights` report repeatedly flags "ended at usage limit before final reporting." That ends with task dirs that contain shippable data products that never moved to `datasets/`. Codex's review (lines 16, 39) measured the cost: `busy/image-similarity-research/` is **11 GB / 457 k entries**. The current rule (`AGENTS.md` §"Task Close-Off" step 4) is correct but lives 200 lines into a doc that is auto-included once per session, and gets skipped under usage pressure. This is process-instruction-as-prevention, which loses to time pressure unless it becomes a mechanical step.

### 4. `resume.md` schema drift makes recovery brittle for the longest-running tasks.

Of 25 resume files, 9 are non-standard. The three "critical in-flight" tasks in `ACTIVE.md` (LLM rethink, LLM detection UI, clustering proposal) include the **empty-template** `llm-detection-ui/resume.md` — the work most expensive to lose has the weakest recovery record. The current `sessionctl reconcile` is the right tool but is human-triggered; a pre-pause / pre-handoff hook or a "starting Claude on a new task" prompt step would catch this.

### 5. `/insights` is high-leverage but ephemeral, provider-local, and not promoted into durable artifacts.

The 2026-05-19 report contains insights the workspace would benefit from forever — multi-clauding overlap, satisfaction-by-pattern, top-error breakdown — but it is an HTML file under `/home/user/.claude/usage-data/`. No task `notes.md` references it; no skill consumes it; Codex can't see it. The user expected `/insights` to work today and was redirected by the lack-of-availability flag. Either `/insights` should be made callable in this environment (out of scope here) or its outputs should be promoted into `investigations/` + `MEMORY.md` whenever it does run.

### 6. Stale claims in `AGENTS.md` are now causing wrong moves.

The 2026-05-20 "the AGENTS.md gotcha says the LLM judge benefits from the full-page screenshot — this is nonsense" event is the clearest signal. `AGENTS.md` is the highest-precedence document in the system reminder, so a stale claim in it propagates everywhere. There is no review cadence on `AGENTS.md` and no "verification-date" convention. Codex's review (line 5) calls out the same risk implicitly by treating it as canonical without question.

## Proposed Skills / Skill Updates

Each entry lists purpose, trigger, source of truth, and anti-staleness rule.

### `workspace-status` (new, shared)
- **Purpose**: emit a single status report joining `ACTIVE.md`, `SESSIONS.md` summary, recent `done/INDEX.md` rows, open PRs, current branch/worktree, gateway routes, and any task that owns the current cwd. Replaces the 6–8 scout commands at session start.
- **Trigger**: agent session start on a non-trivial task; `"where are we"`; `"what's active"`; `"resume"`.
- **Source of truth**: live filesystem + `sessionctl index --json` + `gh pr list --json` + `git worktree list --porcelain`. No cached data.
- **Anti-staleness**: regenerate every call; never persist a copy in the skill.
- **Diff from Codex's `workspace-artifact-inventory`**: that one is for *audit* (counts, drift, cleanup planning); this one is for *daily start-of-session orientation*. Same underlying joins, different reduction.

### `durable-learning-capture` (new, shared) — aligned with Codex's proposal
- **Purpose**: decide where a new rule belongs (AGENTS.md vs shared skill vs knowledge note vs provider memory) and write it with verification metadata. Specifically migrate the existing Claude `~/.claude/projects/-workspace/memory/` into a provider-neutral `detection-platform-metal-work/knowledge/` tree with one-shot mirroring.
- **Trigger**: "remember this", "save a memory", post-mortem learning, repeated gotcha, `/insights` run that surfaces a new pattern.
- **Source of truth**: workspace `knowledge/` tree + `AGENTS.md`.
- **Anti-staleness**: every note must record source artifact, verification date, and a "re-verify before relying on this" condition. Mirror back to `~/.claude/projects/-workspace/memory/MEMORY.md` index so Claude's existing memory loader still picks it up.

### `task-closeoff` (new, shared) — Codex also proposed this
- **Purpose**: enforce the close-off sequence mechanically: verify PR/branch, write `SUMMARY.md`, **harvest data products** out of `busy/<task>/`, update `DAY.md` / `done/INDEX.md`, regenerate sessions, then offer to remove worktree.
- **Trigger**: "close this task off", PR merged, "we're done with X".
- **Source of truth**: `AGENTS.md` close-off section + `ACTIVE.md` keep-rules.
- **Anti-staleness**: cite `AGENTS.md` rather than restate; refuse to close if `busy/<task>/` has data >100 MB unless an explicit harvest step ran.

### `session-hygiene` (new, shared) — Codex also proposed this
- **Purpose**: keep `resume.md`, `SESSIONS.md`, tmux panes, and session IDs aligned. Detect schema drift in existing `resume.md` files.
- **Trigger**: starting/pausing a session, "what's the resume command for X", crash recovery.
- **Source of truth**: `/workspace/tools/agents/sessionctl`.
- **Anti-staleness**: runs `sessionctl reconcile` and `sessionctl index`; never embeds pane lists.

### `agents-md-review` (new, shared, lightweight)
- **Purpose**: scheduled (weekly) lightweight audit of `AGENTS.md` claims — verify any concrete factual claim (e.g., "the LLM judge benefits from the full-page screenshot") still matches code/data. Output a diff PR proposal.
- **Trigger**: `/loop` or `/schedule`-driven cadence; or after a user calls a claim "nonsense".
- **Source of truth**: live repo + datasets.
- **Anti-staleness**: every audited claim gets a `<!-- verified: YYYY-MM-DD against path:line -->` marker; entries without markers older than 30 days are flagged.

### Updates to existing skills
- `detection-dataset-export` / `datasetctl`: when a durable dataset lands, also append a row to `datasets/INDEX.md` automatically (currently `meritking-takedowns-30d-2026-05-14/` and `tether-takedowns-30d-2026-05-14/` have manifests but no INDEX row — Codex's finding).
- `skill-maintainer`: extend with a "promote provider memory → shared knowledge" subcommand for the migration in `durable-learning-capture`.

## What Should NOT Become a Skill

- One-off PR fixes, even recurring-looking ones (e.g., the 2026-05-20 `migrate.sh` bug). The done summary is the right home.
- UI polish per page. Keep in task notes.
- "Run /insights" — Anthropic owns the skill; making a workspace wrapper would just rot.
- A "Claude vs Codex behavior cheat-sheet". Differences should be expressed inline in shared skills (`provider/claude.md`, `provider/codex.md`), not in a meta-document.

## Proposed Knowledge Convention

Match Codex's `detection-platform-metal-work/knowledge/` proposal, with these Claude-side adjustments:

1. **Mirror existing Claude memory** as the seed corpus, one file at a time, preserving the `feedback_*` / `project_*` naming so cross-references survive.
2. **Frontmatter** required: `title`, `tags`, `status` (active|deprecated|under-review), `verified` (YYYY-MM-DD), `source` (path:line or task), `re_verify_when` (free text).
3. **Claude's `MEMORY.md` becomes a thin pointer** to `knowledge/INDEX.md` plus only the truly provider-local rules (e.g., tool-specific quirks). Drop duplicates.
4. **Promotion rule**: a knowledge note that's been used in 2+ tasks and survives a verification re-check graduates to a row in `AGENTS.md` or to a shared skill, whichever fits.
5. **No silent rot**: notes older than 90 days with no verified update are auto-flagged on next `workspace-status` call.

Lookup order for both providers:
`AGENTS.md` → repo `CLAUDE.md` (if scoped) → `knowledge/INDEX.md` → shared skills → provider memory.

## Risks and Open Questions

- **Provider-memory migration is destructive if rushed.** Run it once, in a single task, with a backup of the original `memory/` tree. Claude must still find its rules at session start — keep `MEMORY.md` as a pointer index until the new convention is proven.
- **More skills = more drift.** Each new shared skill needs a verification date; otherwise we'll repeat the AGENTS.md problem at skill scale. The `agents-md-review` skill should cover skills too.
- **`/insights` is the best signal we have but it's not in this environment.** Worth checking: is `/insights` part of an Anthropic-managed skill bundle that we should enable as a plugin in this workspace? If not, we can approximate its key sections with a custom skill that re-reads transcripts under `~/.claude/projects/-workspace/` — but transcript-format stability is an Anthropic-internal concern, so this would be brittle.
- **`workspace-status` scope creep.** Hard-cap at 200 lines of output. The point is to replace 8 commands with 1, not to dump everything.
- **The "ultrathink" tax (128 instances over 15 sessions) is partly a model-quality problem, not a workspace problem.** Workspace changes can reduce the rediscovery-induced share of it; they cannot eliminate the genuine-hard-problem share.
- **Open**: do any current Claude task dirs use a resume.md format that `sessionctl` parses *because* it's Claude-generated, but Codex's writer can't reproduce? Worth a one-task audit before declaring the schema cross-provider.
