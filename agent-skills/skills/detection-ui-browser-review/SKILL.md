---
name: detection-ui-browser-review
description: Review the detection-ui frontend through the local workspace gateway using the shared Playwright browser MCP wrapper, preserving screenshots and findings in task artifacts.
---

# Detection UI Browser Review

Use this skill when reviewing, debugging, or visually validating the
`detection-ui` frontend with a browser in this workspace.

## Guardrails

- Use local stack URLs only. Do not validate detection-ui work against staging or
  production HTTP endpoints.
- Start and route local UI instances through `/workspace/tools/gateway/gatewayctl`.
- Multiple local UI stacks are supported. Use one unique stack name and one
  unique loopback IP per worktree; reserve `127.0.0.1` for the gateway listener.
- Use `/workspace/tools/browser-mcp/browser-mcp detection-ui` for browser MCP
  access. The wrapper defaults to the Playwright Docker runtime when the image is
  available locally.
- Save screenshots and browser artifacts under the active task's
  `screenshots/` directory. For standalone investigations, use
  `/workspace/detection-platform-metal-work/investigations/<topic>/screenshots/`.
- Treat browser MCP review as exploratory validation. Keep container-based unit,
  frontend, and Playwright e2e tests as the regression checks for code changes.

## Workflow

1. Identify the target UI URL:
   ```bash
   /workspace/tools/gateway/gatewayctl status
   /workspace/tools/gateway/gatewayctl stack list
   /workspace/tools/gateway/gatewayctl url <name>
   ```
   Use URLs shaped like `http://<name>.localhost:18000/`.
2. If the stack is not running, start it through the gateway with a unique
   stack name and loopback IP:
   ```bash
   /workspace/tools/gateway/gatewayctl stack up <name> <worktree-path> 127.0.0.N \
     --tag <tag> \
     --service detection-ui-frontend
   ```
   Add repeatable `--service <svc>` targets only when the review requires them,
   for example `--service classifier-worker` for Classifier Data or
   brand-corpus checks. Use `--all` only when every Compose service is required.
   Use `--no-build` only when the selected local images already exist.
3. Prepare artifact output before launching the agent client or browser MCP:
   ```bash
   mkdir -p /workspace/detection-platform-metal-work/busy/<task>/screenshots
   export AGENT_BROWSER_OUTPUT_DIR=/workspace/detection-platform-metal-work/busy/<task>/screenshots
   ```
   If the browser is being used for a standalone investigation, put the
   screenshot directory under `investigations/<topic>/screenshots/` instead.
4. Use the browser MCP to navigate and inspect the UI. Prefer accessibility
   snapshots for structure and targeted screenshots for layout, clipping,
   overflow, visual regressions, and responsive states.
5. Record findings with the evidence needed for another agent to resume:
   target URL, route, viewport, screenshot paths, console/network errors, and
   relevant source file references.
6. If code changed, run the appropriate Docker-backed validation from the repo
   instructions. Do not replace tests with browser exploration.

## Useful Commands

```bash
/workspace/tools/gateway/gatewayctl status
/workspace/tools/gateway/gatewayctl stack list
/workspace/tools/gateway/gatewayctl doctor
/workspace/tools/browser-mcp/browser-mcp --help
docker image inspect mcr.microsoft.com/playwright:v1.58.2-noble >/dev/null
```

`gatewayctl stack --help` is not a supported help command; use
`/workspace/tools/gateway/gatewayctl --help` for stack option syntax.

For the current shared browser MCP wrapper docs, read:

```bash
sed -n '1,220p' /workspace/tools/browser-mcp/README.md
```
