---
title: "Playwright MCP must run headless"
description: "Playwright MCP must be configured with --headless flag for headless Chrome in Docker containers without X server"
tags: [feedback, memory-migration]
status: active
verified: 2026-05-20
source: "sanitized workspace memory migration, 2026-05-20"
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation."
---

The Playwright MCP plugin config (`.mcp.json`) is read ONLY at Claude Code session start. The `/mcp` reconnect command does NOT re-read config files — it restarts the same cached command.

**Why:** This sandbox has no X server (headless Docker container). The default Playwright MCP launches Chrome in headed mode which fails.

**How to apply:** Claude Playwright MCP configuration files for this workspace must include `--headless` in args. This was set on 2026-03-26 and should persist across sessions. If it breaks again, inspect the provider-local Playwright MCP configs and confirm the launched browser is headless.
