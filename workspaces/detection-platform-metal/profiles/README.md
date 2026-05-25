# Detection Platform Metal Profiles

Profiles describe task-oriented bundles of overlays, skills, tools, and
guardrails. They are source descriptions, not provider runtime profiles yet.

Candidate profiles:

- `review`: read-only branch, PR, or plan review.
- `implementation`: worktree-based implementation with Docker validation.
- `db-investigation`: production read-only DB investigation via `dbctl`.
- `ui-review`: local UI/browser review with screenshots under task artifacts.
- `dataset-export`: incident scope exports and dataset manifests.
- `workspace-maintenance`: skill sync, knowledge sync, task/session hygiene.

Provider adapters may translate these profiles into Claude prompts, Codex custom
agents, or Pi workflows.
