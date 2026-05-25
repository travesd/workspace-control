---
name: workspace-artifact-inventory
description: Generate an audit-grade inventory of workspace tasks, sessions, worktrees, datasets, backups, skills, and known drift.
---

# Workspace Artifact Inventory

Use this skill for cleanup planning, organization reviews, or before broad archiving.

## Workflow

1. Run `tools/workspace-artifact-inventory` from this repo when available.
2. Save the inventory under the active task or investigation.
3. Include counts and drift:
   - busy/done/later/archived/investigation directories,
   - resume files and missing resumes,
   - session warnings,
   - worktrees,
   - dataset and backup manifests,
   - shared skill inventory,
   - large task directories.

## Guardrails

- Inventory is read-only.
- Do not move or delete anything during inventory.
- Treat generated output as point-in-time evidence.
