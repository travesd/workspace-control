# Skill Parameterization Live Activation Plan

Date: 2026-05-25

Status: proposed; not activated

## Objective

Activate the reviewed shared-skill improvements from
`/workspace/workspace-control` into the live `/workspace` Claude/Codex skill
surfaces without changing always-loaded instructions, product repositories,
active chats, Pi files, or provider runtime config.

This plan covers the repo state at:

```text
330d7a7 docs(workspace): split call-a-friend provider commands
```

Relevant reviewed commits:

- `e807a12 docs(workspace): parameterize core learning skills`
- `330d7a7 docs(workspace): split call-a-friend provider commands`

Review evidence:

- Claude `ultrareview c3a1da1 --timeout 20` completed on 2026-05-25 and
  reported no findings after refuting three candidate issues.
- `tools/renderctl dry-run --mode all`, `--mode skills`, and
  `--mode providers` were clean.
- Compatibility and generated skill trees validated with `skillctl validate`.

## Scope

In scope:

- Sync `/workspace/workspace-control/agent-skills/skills/` to
  `/workspace/agent-skills/skills/`.
- Run `/workspace/tools/skills/skillctl validate`.
- Run `/workspace/tools/skills/skillctl sync` to regenerate Claude and Codex
  skill mirrors.
- Optionally copy two documentation-only live tool README files so
  `live-check` can reach a clean state:
  - `current-workspace/tools/README.md` -> `/workspace/tools/README.md`
  - `current-workspace/tools/skills/README.md` ->
    `/workspace/tools/skills/README.md`

Out of scope:

- No changes to `/workspace/AGENTS.md` or `/workspace/CLAUDE.md`.
- No changes to product repositories or worktrees.
- No task lifecycle movement.
- No Pi activation or `.pi/settings.json` changes.
- No provider adapter runtime config changes.
- No interruption, restart, resume, or closure of active Claude/Codex chats.

## Current Live-Check

Fresh check on 2026-05-25:

```bash
cd /workspace/workspace-control
tools/renderctl dry-run --mode live-check
```

Expected pre-activation result: nonzero.

Current drift:

- `/workspace/AGENTS.md`: clean.
- `/workspace/CLAUDE.md`: clean.
- `/workspace/tools/`: only missing `README.md` and `skills/README.md`.
- `/workspace/agent-skills/skills/`: live skill tree lags repo skill tree.
- `/workspace/.claude/skills/`: mirror lags repo skill tree.
- `/workspace/.agents/skills/`: mirror lags repo skill tree.

## Preflight

Run from `/workspace/workspace-control`:

```bash
git status --short --branch
git rev-parse HEAD
./tools/check-sensitive-content .
./tools/renderctl dry-run --mode all
./tools/renderctl dry-run --mode skills
./tools/renderctl dry-run --mode providers
SKILLCTL_CANONICAL_DIR=/workspace/workspace-control/agent-skills/skills \
  /workspace/tools/skills/skillctl validate
out="$(mktemp -d /tmp/workspace-control-generated-skills.XXXXXX)"
./tools/renderctl dry-run --mode skills --out "$out"
SKILLCTL_CANONICAL_DIR="$out/rendered/agent-skills/skills" \
  /workspace/tools/skills/skillctl validate
rm -rf "$out"
./tools/renderctl dry-run --mode live-check
```

The last command is expected to return nonzero before activation. Record the
diff summary in the task notes.

## Rollback Snapshot

Before live mutation:

```bash
TASK=/workspace/detection-platform-metal-work/busy/workflow-improvements-go-live-20260521
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ROLLBACK="$TASK/rollback/$STAMP-before-skill-parameterization-activation"
mkdir -p "$ROLLBACK"

cp -a /workspace/agent-skills "$ROLLBACK/agent-skills"
cp -a /workspace/.claude/skills "$ROLLBACK/claude-skills"
cp -a /workspace/.agents/skills "$ROLLBACK/openai-skills"
if [ -f /workspace/tools/README.md ]; then
  cp -a /workspace/tools/README.md "$ROLLBACK/tools-README.md"
fi
if [ -f /workspace/tools/skills/README.md ]; then
  cp -a /workspace/tools/skills/README.md "$ROLLBACK/tools-skills-README.md"
fi

find /workspace/agent-skills/skills -type f -print | sort > "$ROLLBACK/agent-skills-files.before.txt"
find /workspace/.claude/skills -type f -print | sort > "$ROLLBACK/claude-skills-files.before.txt"
find /workspace/.agents/skills -type f -print | sort > "$ROLLBACK/openai-skills-files.before.txt"
sha256sum /workspace/AGENTS.md /workspace/CLAUDE.md > "$ROLLBACK/instruction-checksums.before.txt"
```

Write a short `MANIFEST.md` in the rollback directory that names:

- source repo commit,
- activation timestamp,
- copied rollback paths,
- exact activation commands run,
- post-activation validation result.

## Activation Commands

Run only after explicit user approval for live activation.

```bash
cd /workspace/workspace-control

rsync -a --delete \
  /workspace/workspace-control/agent-skills/skills/ \
  /workspace/agent-skills/skills/

/workspace/tools/skills/skillctl validate
/workspace/tools/skills/skillctl sync
```

Optional tool documentation parity:

```bash
install -m 664 \
  /workspace/workspace-control/current-workspace/tools/README.md \
  /workspace/tools/README.md
install -m 664 \
  /workspace/workspace-control/current-workspace/tools/skills/README.md \
  /workspace/tools/skills/README.md
```

## Post-Activation Validation

```bash
cd /workspace/workspace-control
/workspace/tools/skills/skillctl validate
/workspace/tools/skills/skillctl inventory
./tools/renderctl dry-run --mode live-check
```

Expected post-activation result:

- If optional tool documentation parity is included, `live-check` should be
  clean for instructions, tools, canonical skills, and provider mirrors.
- If optional tool documentation parity is skipped, `live-check` should only
  report the two missing tool README files.

Fresh already-running Claude/Codex sessions may not reload skill metadata until
they are restarted or resumed. Validate behavior from a fresh session if needed.

## Rollback Commands

Run only if post-activation validation fails or the user asks to revert:

```bash
ROLLBACK=<rollback-dir>

rsync -a --delete "$ROLLBACK/agent-skills/" /workspace/agent-skills/
rsync -a --delete "$ROLLBACK/claude-skills/" /workspace/.claude/skills/
rsync -a --delete "$ROLLBACK/openai-skills/" /workspace/.agents/skills/

if [ -f "$ROLLBACK/tools-README.md" ]; then
  cp -a "$ROLLBACK/tools-README.md" /workspace/tools/README.md
else
  rm -f /workspace/tools/README.md
fi
if [ -f "$ROLLBACK/tools-skills-README.md" ]; then
  cp -a "$ROLLBACK/tools-skills-README.md" /workspace/tools/skills/README.md
else
  rm -f /workspace/tools/skills/README.md
fi

/workspace/tools/skills/skillctl validate
cd /workspace/workspace-control
./tools/renderctl dry-run --mode live-check
```

After rollback, record the result in the task notes and rollback manifest.

## Recommendation

Activate the shared-skill sync and the two documentation-only tool README files
together. That keeps the mutation limited to reviewed operating-model surfaces
and should make `renderctl --mode live-check` clean afterward without touching
always-loaded instructions, Pi, product repos, or active chats.
