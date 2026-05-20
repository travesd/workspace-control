# External References

Checked: 2026-05-20

These references informed the recommendations but did not override workspace evidence.

## Agent Memory And Skills

- OpenAI Codex customization: https://developers.openai.com/codex/concepts/customization
  - Relevant point: `AGENTS.md`, memories, skills, MCP, and subagents are complementary layers; skills are the right layer for repeatable workflows.
- OpenAI Codex memories: https://developers.openai.com/codex/memories
  - Relevant point: memories are useful local recall, but required team rules belong in `AGENTS.md` or checked-in documentation.
- Claude Code memory: https://code.claude.com/docs/en/memory
  - Relevant point: keep always-loaded instructions concise and specific; use skills for multi-step procedures; auto memory uses an indexed `MEMORY.md` plus topic files.

## Decision Records

- MIT Libraries ADR guide: https://mitlibraries.github.io/guides/misc/adr.html
  - Relevant point: ADRs should capture one decision with title, status, context, decision, and consequences.
- ADR overview: https://adr.github.io/
  - Relevant point: decision records form a decision log that preserves rationale, tradeoffs, and consequences.

## Note-Taking Conventions

No broad external note-taking framework should be adopted wholesale from this pass. The useful subset is:

- short index,
- atomic notes,
- tags/frontmatter,
- source/provenance,
- verification date,
- backlinks to task artifacts.
