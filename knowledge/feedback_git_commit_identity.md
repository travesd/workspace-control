---
title: "feedback git commit identity"
tags: [imported, claude-memory, feedback]
status: active
verified: 2026-05-20
source: /home/user/.claude/projects/-workspace/memory/feedback_git_commit_identity.md
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation"
---

---
name: feedback-git-commit-identity
description: "Never override the git commit author/committer identity — always use the configured git config (currently travesd via privacy noreply). No --author flag, no GIT_AUTHOR/COMMITTER_* env vars, no `git -c user.email=...`."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 20c69ebd-3dbf-4610-8042-aad3fdf2a9c8
---

When making a commit, **always use the identity from `git config`** as-is. Do not override it.

**Why:** the user's `~/.gitconfig` is intentionally set to `travesd <58914721+travesd@users.noreply.github.com>` — the GitHub privacy noreply that ties commits to their `travesd` account. They have a second GitHub account (`pfmailyer`) that has `travis.ford@phishfort.com` as a verified email. If a commit uses the real email as the author, GitHub attributes it to `pfmailyer` instead of `travesd` — breaking PR attribution. This happened on PR #63 (commits `f1eb012e`, `a09d3505`, plus `dba9a123` which landed on main via PR #81). The user reaction was direct: "who the fuck is changing who we commit as? we should be using the git config fucking ALWAYS … this breaks attribution."

**How to apply:**
- Run `git commit` and `git merge` with no identity-override flags. Let git read `~/.gitconfig` / repo-local config.
- Do not use `--author=...`. Do not set `GIT_AUTHOR_EMAIL` / `GIT_AUTHOR_NAME` / `GIT_COMMITTER_EMAIL` / `GIT_COMMITTER_NAME`. Do not run `git -c user.email=... commit`.
- The auto-memory entry `userEmail = travis.ford@phishfort.com` is metadata about the user's identity for memory/context use. It is **not** the value to pass to git. Ignore it for commits.
- The `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>` trailer in the commit message body is fine and required by [[feedback-pr-default-base-main]] / AGENTS.md — that does not change primary attribution.
- Before committing, you can sanity-check with `git config --get user.email` — should be `58914721+travesd@users.noreply.github.com`. If it isn't, stop and ask before committing.
- If you see a prior commit in a branch you're touching that used the wrong identity, flag it; don't silently propagate. The fix is `git commit --amend --reset-author --no-edit` (or rebase with `--reset-author` for older commits) followed by a force-push the user has explicitly approved.
