---
name: history
description: Update YuBan's docs/HISTORY.md from meaningful Git commit history. Use when asked to record project development history or bring HISTORY.md up to date; do not use for a raw commit log or release notes in another format.
---

# YuBan history

Maintain `docs/HISTORY.md` as a concise, reader-oriented development record grounded in Git history.

## Gather evidence

1. Read the current `docs/HISTORY.md`, its recent modifying commits, and the working-tree status.
   If the history file already has uncommitted edits, inspect and preserve them; do not duplicate their coverage or overwrite unrelated work.
2. Unless the request gives a range, use the commit that most recently changed `docs/HISTORY.md` as the baseline. Inspect the commits after it with dates, subjects, changed files, and diffs as needed.
3. Exclude merge commits when identifying changes. Use them only to understand branch context when a non-merge commit is unclear.
4. Inspect commits beyond their subject lines before describing outcomes, especially for resource data, workflow, security, and deployment changes.

## Write the history

- Group related, user-meaningful changes by date. Add to an existing date when later commits belong there; put newer dates before older ones.
- Preserve the document's existing title, introduction, language, and entry format unless the user asks to revise them.
- Summarize outcomes and important process changes; omit routine chores, duplicate commits, and implementation noise unless they materially change how the project is used or maintained.
- State only what the commits demonstrate. Do not invent release status, review status, deployment success, or metrics.
- Update an earlier entry when subsequent commits on that date materially complete or correct its story instead of adding overlapping bullets.

## Verify

Review `git diff --check` and the final `docs/HISTORY.md` diff. Confirm each added claim maps to one or more inspected commits and that no unrelated working-tree changes were modified. Report the date range and the main groups recorded.
