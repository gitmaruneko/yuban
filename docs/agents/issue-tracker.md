# Issue tracker: GitHub

Issues and PRDs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- Create, read, list, comment on, label, and close issues with `gh issue` commands.
- Infer the repository from the GitHub `origin` remote.
- Pull requests as a triage surface: no.
- When a skill says "publish to the issue tracker", create a GitHub issue.
- When a skill says "fetch the relevant ticket", read the issue body, comments, and labels.
- Use GitHub native issue dependencies for blocking edges; fall back to a `Blocked by` line when unavailable.