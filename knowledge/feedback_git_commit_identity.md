---
title: "Never override git commit identity"
description: "Never override the git commit author/committer identity. Use the repository or user git config as-is. No --author flag, no GIT_AUTHOR/COMMITTER_* env vars, no `git -c user.email=...`."
type: feedback
tags: [feedback, memory-migration]
status: active
scope: workspace
verified: 2026-05-20
source: "sanitized workspace memory migration, 2026-05-20"
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation."
---

When making a commit, **always use the identity from `git config`** as-is. Do not override it.

**Why:** this workspace relies on the configured git identity for correct PR attribution. Overriding the author or committer can attribute commits to the wrong account and force history repair.

**How to apply:**
- Run `git commit` and `git merge` with no identity-override flags. Let git read `~/.gitconfig` / repo-local config.
- Do not use `--author=...`. Do not set `GIT_AUTHOR_EMAIL` / `GIT_AUTHOR_NAME` / `GIT_COMMITTER_EMAIL` / `GIT_COMMITTER_NAME`. Do not run `git -c user.email=... commit`.
- Ignore provider memory or profile metadata when choosing commit identity.
- Provider attribution trailers in the commit message body do not change primary git attribution.
- Before committing, you can sanity-check with `git config --get user.email`. If the configured value looks wrong for the repo, stop and ask before committing.
- If you see a prior commit in a branch you're touching that used the wrong identity, flag it; don't silently propagate. The fix is `git commit --amend --reset-author --no-edit` (or rebase with `--reset-author` for older commits) followed by a force-push the user has explicitly approved.
