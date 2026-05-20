---
title: "feedback playwright headless"
tags: [imported, claude-memory, feedback]
status: active
verified: 2026-05-20
source: /home/user/.claude/projects/-workspace/memory/feedback_playwright_headless.md
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation"
---

---
name: playwright-mcp-headless
description: Playwright MCP must be configured with --headless flag for headless Chrome in Docker containers without X server
type: feedback
---

The Playwright MCP plugin config (`.mcp.json`) is read ONLY at Claude Code session start. The `/mcp` reconnect command does NOT re-read config files — it restarts the same cached command.

**Why:** This sandbox has no X server (headless Docker container). The default Playwright MCP launches Chrome in headed mode which fails.

**How to apply:** All `.mcp.json` files under `~/.claude/plugins/**/playwright/` must have `--headless` in args. This was set on 2026-03-26 and should persist across sessions. If it breaks again, check all cached configs:
```bash
find ~/.claude -name ".mcp.json" -path "*playwright*" -exec cat {} \;
```
