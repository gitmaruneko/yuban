Commit-and-push script

Usage (PowerShell):

```powershell
# default: stages all, commits with message, pushes
./tools/commit_and_push/commit-and-push.ps1 -Message "chore: init project"

# skip staging (useful if you staged manually)
./tools/commit_and_push/commit-and-push.ps1 -All:$false -Message "fix: ..."

# force push and skip hooks
./tools/commit_and_push/commit-and-push.ps1 -Force -Message "chore: force push"
```

Notes:
- Requires `git` in PATH.
- Run from within the repository (script resolves repo root automatically).
