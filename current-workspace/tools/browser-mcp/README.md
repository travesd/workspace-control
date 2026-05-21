# Browser MCP Wrapper

`browser-mcp` is workspace-owned agent tooling for browser review. It runs a
pinned Playwright MCP server with an isolated browser profile and guardrails for
artifact placement.

This is not repo application code. It is safe to run on the host under the
workspace execution model because agents run on the host while
`detection-platform-metal` services run in Docker.

## Usage

For detection-ui review, start the local stack through the gateway, then expose
an artifact directory before starting the agent client:

```bash
mkdir -p /workspace/detection-platform-metal-work/busy/<task>/screenshots
export AGENT_BROWSER_OUTPUT_DIR=/workspace/detection-platform-metal-work/busy/<task>/screenshots
/workspace/tools/browser-mcp/browser-mcp detection-ui
```

The `detection-ui` profile is intended for gateway URLs such as:

```text
http://domain-llm-v2.localhost:18000/
```

When `AGENT_BROWSER_OUTPUT_DIR` is unset, the wrapper starts in stdout output
mode so accessibility snapshots and normal browser interaction still work. Set
`AGENT_BROWSER_OUTPUT_DIR` before launching Claude or Codex when screenshots or
saved browser artifacts are part of the task.

## Recovery

If a browser MCP tool call fails with `Transport closed`, the stdio connection
inside the already-running agent client cannot be reconnected from inside that
chat. Clean up stale Playwright MCP runtimes, then restart or resume the agent
client from `/workspace` so it opens a fresh MCP transport:

```bash
/workspace/tools/browser-mcp/browser-mcp doctor
/workspace/tools/browser-mcp/browser-mcp cleanup
```

Use a dry run first when other agents may be actively using browser MCP:

```bash
/workspace/tools/browser-mcp/browser-mcp cleanup --dry-run
```

The cleanup command only targets Playwright MCP containers/processes. It does
not stop the local gateway, detection-ui stacks, DB tunnels, or application
containers.

## Claude Project MCP

Project-scoped Claude configuration can use:

```json
{
  "mcpServers": {
    "detection-browser": {
      "type": "stdio",
      "command": "/workspace/tools/browser-mcp/browser-mcp",
      "args": ["detection-ui"],
      "env": {
        "AGENT_BROWSER_OUTPUT_DIR": "${AGENT_BROWSER_OUTPUT_DIR:-}",
        "AGENT_BROWSER_ALLOWED_ORIGINS": "${AGENT_BROWSER_ALLOWED_ORIGINS:-}",
        "AGENT_BROWSER_BLOCKED_ORIGINS": "${AGENT_BROWSER_BLOCKED_ORIGINS:-}"
      }
    }
  }
}
```

## Codex Project MCP

Project-scoped Codex configuration can use:

```toml
[mcp_servers.detection-browser]
command = "/workspace/tools/browser-mcp/browser-mcp"
args = ["detection-ui"]
env_vars = [
  "AGENT_BROWSER_OUTPUT_DIR",
  "AGENT_BROWSER_ALLOWED_ORIGINS",
  "AGENT_BROWSER_BLOCKED_ORIGINS",
  "AGENT_BROWSER_VIEWPORT",
  "PLAYWRIGHT_MCP_VERSION",
]
startup_timeout_sec = 20
tool_timeout_sec = 120
enabled = true
```

## Notes

- Default Playwright MCP version: `0.0.73`.
- Override with `PLAYWRIGHT_MCP_VERSION` only when deliberately testing a new
  server release.
- Default runtime is `auto`. It uses the Playwright Docker runtime when
  `mcr.microsoft.com/playwright:v1.58.2-noble` is available locally; otherwise
  it falls back to host `npx`.
- Pre-pull the Docker runtime to avoid MCP startup delays:
  ```bash
  docker pull mcr.microsoft.com/playwright:v1.58.2-noble
  ```
- For host runtime, the wrapper auto-detects Playwright-managed Chromium under
  `$HOME/.cache/ms-playwright/`. If the cache is empty, install it with:
  ```bash
  npx -y playwright@1.60.0-alpha-1777669338000 install chromium
  ```
- Override runtime with `AGENT_BROWSER_RUNTIME=docker` or
  `AGENT_BROWSER_RUNTIME=host`.
- Override browser selection with `AGENT_BROWSER_EXECUTABLE_PATH` when needed.
- Keep screenshots in `busy/<task>/screenshots/` or
  `investigations/<topic>/screenshots/`.
- Use Playwright MCP for exploratory browser review. Keep repo Playwright e2e
  tests as validation for stable behavior.
