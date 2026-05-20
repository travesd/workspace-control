---
name: Use e.code not e.key for keyboard shortcuts with modifiers
description: e.key returns the shifted character (Shift+. = ">"), breaking shortcut detection. e.code returns the physical key. Playwright bypasses this.
type: feedback
---

When implementing keyboard shortcuts that use Shift as a modifier, use `e.code` (physical key, e.g. `"Period"`) not `e.key` (character produced, e.g. `">"` when Shift is held).

**Why:** `Shift+.` produces `e.key === ">"`, not `"."`. A check like `e.ctrlKey && e.shiftKey && e.key === "."` will never match in a real browser. Playwright synthetic key events bypass OS key mapping, so automated tests pass while real users can't trigger the shortcut.

**How to apply:** Any time you write a keydown handler that checks `e.key` alongside `e.shiftKey`, switch to `e.code`. Common mappings: `"Period"`, `"Comma"`, `"Slash"`, `"BracketLeft"`, etc.
