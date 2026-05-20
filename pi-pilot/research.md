# Pi Pilot Research Notes

Checked: 2026-05-20

## Relevant Pi Capabilities

- Pi is a minimal terminal coding harness extended through TypeScript extensions, skills, prompt templates, themes, and packages.
- Pi can load Agent Skills from project-local `.pi/skills/`, `.agents/skills/`, global skill dirs, package-provided skills, settings, and CLI flags.
- Pi agent files live under project `.pi/agents/**/*.md`; Pi subagent packages also discover legacy `.agents/**/*.md`.
- Pi workflow graphs can use `spawn`, `sequence`, `fork`, `join`, and `loop`.
- Some Pi packages persist flows and harness artifacts for auditability.
- Pi's skills docs explicitly warn that skills can instruct arbitrary actions and include executable code; review skill content before use.

## Workspace Interpretation

Use Pi to model repeatable coordination patterns that already work in Claude/Codex:

- scout current state,
- run parallel review streams,
- cross-review findings,
- synthesize recommendations,
- write durable task artifacts.

Do not use Pi to replace the source of truth. The source of truth should remain root docs, `knowledge/`, and shared skills in this repo.

## Sources

- Pi docs: `https://pi.dev/docs/latest`
- Pi skills docs: `https://pi.dev/docs/latest/skills`
- `pi-agents`: `https://pi.dev/packages/pi-agents`
- `pi-subagents`: `https://pi.dev/packages/pi-subagents`
- `ultimate-pi`: `https://pi.dev/packages/ultimate-pi`
