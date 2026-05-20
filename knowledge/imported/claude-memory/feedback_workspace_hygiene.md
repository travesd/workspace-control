---
name: Workspace hygiene enforcement
description: Always create busy/<task>/ directory BEFORE generating any work artifacts - never dump files in workspace root or detection-platform-work root
type: feedback
---

Always follow workspace organisation rules from the start of a task, not as an afterthought.

**Why:** User was frustrated when intermediate data files (JSON exports, scripts, HTML reports) were dumped directly into `/workspace/detection-platform-work/` root instead of a proper `busy/<task-name>/` directory. This pollutes the workspace.

**How to apply:** At the very start of any task that will produce files, create `busy/<task-name>/` and put ALL artifacts there from the beginning — data exports, scripts, reports, intermediate files, everything. Don't create files first and reorganise later.
