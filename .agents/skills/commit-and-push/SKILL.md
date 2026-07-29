# commit-and-push Skill

Purpose
- Provide a lightweight, repository-local "skill" that documents and wraps the `commit-and-push` workflow so developers and local agents can run a safe, repeatable commit + push operation.

What it does
- Documents the `tools/commit_and_push/commit-and-push.ps1` script and its parameters.
- Shows cross-platform invocation options and CI usage examples.
- Lists safe defaults, required confirmations, and security guidance for agent integration.

Files touched
- `tools/commit_and_push/commit-and-push.ps1` (PowerShell script)
- `tools/commit_and_push/README.md`

Script parameters & behavior
- `-Message <string>`: commit message (default: "chore: update").
- `-All` / `-All:$false`: stage all changes by default; pass `-All:$false` to skip staging.
- `-Force`: skip pre-commit hooks and optionally force-push when true.
- Behavior: resolves repo root, optionally stages changes, commits if there are changes, then pushes current branch to `origin`.

Usage examples
- PowerShell (Windows):

  ```powershell
  ./tools/commit_and_push/commit-and-push.ps1 -Message "chore: save changes"
  ```

- PowerShell Core (cross-platform):

  ```bash
  pwsh ./tools/commit_and_push/commit-and-push.ps1 -Message "chore: save changes"
  ```

- Bash wrapper (optional): create `tools/commit_and_push/commit-and-push.sh` that calls `pwsh` to run the PowerShell script for environments without native PowerShell.

CI example (GitHub Actions)

```yaml
name: Commit and Push
on: workflow_dispatch
jobs:
  commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run commit-and-push
        env:
          GIT_AUTHOR_NAME: github-actions
          GIT_AUTHOR_EMAIL: github-actions@github.com
        run: |
          pwsh ./tools/commit_and_push/commit-and-push.ps1 -Message "chore: CI auto-commit"
```

Agent integration notes
- Agents invoking this skill must always request explicit user confirmation before using `-Force` or performing a force-push.
- Prefer a two-step flow: (1) show a summary of staged/unstaged changes, (2) prompt user to confirm commit message and push.
- Do not store or print tokens in logs; use environment variables for CI credentials.

Security & safety
- Avoid hardcoding tokens or credentials in the script. Read them from environment variables when needed.
- The script should not run automatically without user consent when used by interactive agents.

Recommended skill name
- `commit-and-push`

Notes
- This skill is intentionally lightweight and repository-local. For deeper integration (VS Code command, extension, or a hosted agent skill), create the appropriate metadata or extension that references this folder and enforces interactive confirmations.
