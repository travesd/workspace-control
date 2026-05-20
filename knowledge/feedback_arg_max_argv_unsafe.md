---
title: "ARG_MAX — large strings in argv are unsafe above ~128 KB"
description: "Any shell command where a large value goes into argv (curl -d, jq --argjson, python -c, etc.) will fail with \"Argument list too long\" above ~128 KB; use tempfile or stdin"
tags: [feedback, memory-migration]
status: active
verified: 2026-05-20
source: "sanitized workspace memory migration, 2026-05-20"
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation."
---

Any shell pattern that passes a large string as a command-line argument — `curl -d "$data"`, `jq --argjson map "$big"`, `python -c "$script"`, `-e VAR=<huge>` on docker run — is ARG_MAX-unsafe above roughly 128 KB, and FAILS LOUDLY AND MISLEADINGLY on larger inputs. Rewrite to use a file or stdin instead.

**Why:** Hit this three times in one task (`migrate-sh-data-sync`, PR metal#7):
1. `jq --argjson p "$page"` in pagination accumulator → `Argument list too long` on 25 MB snapshot JSON page.
2. `jq --argjson map "$big_map"` for snapshot id remap → same.
3. `curl -d "$data"` in `_post`/`_put`/`_delete`/`_patch` helpers → same, on the same 25 MB snapshot body.

Failure mode #3 was especially brutal: exec fails before curl runs, bash emits `infrastructure/docker/migrate.sh: line N: /usr/bin/curl: Argument list too long` to stderr, the subshell's `2>&1` captures it into the response variable, subsequent `$(echo "$response" | tail -1)` extracts a non-numeric word as `$status`, and `[[ "$status" -ge 400 ]]` does arithmetic on the string — which under `set -u` blows up with `infrastructure: unbound variable` (treating "infrastructure" as a variable reference). Silent data corruption with misleading errors.

**How to apply:**
- **jq accumulation**: instead of `acc=$(echo "$acc" | jq --argjson p "$page" '. + $p')`, write both to tempfiles and use `jq -s '.[0] + .[1]' acc.json page.json`.
- **curl POST/PATCH bodies**: `-d @/tmp/body.json` instead of `-d "$data"`. A helper like `_body_tmp() { t=$(mktemp); printf '%s' "$1" > "$t"; echo "$t"; }` keeps the call site readable.
- **Defensive pattern for any `-d` / `--argjson` consumer**: also add `[[ "$status" =~ ^[0-9]+$ ]]` (or equivalent language-level check) before arithmetic — so if ARG_MAX fires somewhere you forgot, you get a clear error instead of "unbound variable".
- **Heuristic**: if a payload can realistically exceed ~128 KB (JSON with embedded DOM/HTML/screenshots, large corpora, multi-MB classifier manifests), assume argv is unsafe and choose file or stdin from the start.

**Rule of thumb for "how big"**: Linux x86_64 ARG_MAX is typically 2 MB (`getconf ARG_MAX`), but the effective limit accounting for environment variables is often closer to 128 KB. Don't cut it close — anything above ~64 KB should already be going through a file.
