# commit-and-push script

A lightweight repository-local helper that wraps a simple `git add`, `git commit`, and `git push` workflow.

## Behavior

- Resolves the repository root automatically before running.
- By default stages all local changes with `git add -A`.
- Commits the current working tree if there are staged or uncommitted changes.
- Pushes the current branch to `origin` after committing.

## Parameters

- `-Message <string>`: commit message. Default: `"chore: update"`.
- `-All`: stage all changes automatically before committing. This is the default behavior.
- `-All:$false`: do not stage files automatically; use this if you want to manage staging manually.
- `-Force`: adds `--no-verify` to the commit command and uses `git push --force`.

## Usage

```powershell
# default: stage all changes, commit, push
./tools/commit_and_push/commit-and-push.ps1 -Message "chore: init project"

# skip automatic staging when you already staged specific files manually
./tools/commit_and_push/commit-and-push.ps1 -All:$false -Message "fix: update README"

# force commit without hooks and force-push
./tools/commit_and_push/commit-and-push.ps1 -Force -Message "chore: force push"
```

## Notes

- Requires `git` in `PATH`.
- The script resolves the repo root automatically, so you can run it from any folder inside the repository.
- Examples are PowerShell-specific; use `pwsh` on non-Windows platforms.
- The script is intentionally kept as a PowerShell canonical implementation. If you need a non-PowerShell wrapper, create a small shell script that invokes `pwsh ./tools/commit_and_push/commit-and-push.ps1`.

## Safety

- Avoid hardcoding credentials or tokens inside this script.
- Do not use `-Force` without explicit review of the changes and confirmation from the user.
- In CI, inject credentials through environment variables and do not print secrets to logs.
