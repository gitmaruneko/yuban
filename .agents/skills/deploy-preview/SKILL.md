# deploy-preview Skill

Purpose
- Deploy the current YuBan source to the shared `yuban-preview` GitHub Pages site and verify that the published site matches the requested source.

Scope
- This skill only deploys and verifies a preview. It does not commit, push, merge, or deploy the production site.
- Use `commit-and-push` first when the source changes are not already pushed.

Canonical command

```powershell
./tools/deploy_preview/deploy-preview.ps1 -SourceRef feature/your-branch
```

The script resolves the source branch to a full commit SHA before dispatching `gitmaruneko/yuban-preview`'s `Deploy preview` workflow. Passing a full SHA is also supported:

```powershell
./tools/deploy_preview/deploy-preview.ps1 -SourceRef 0123456789abcdef0123456789abcdef01234567
```

Workflow
1. Confirm the source branch or commit exists on `origin`.
2. Resolve the source to a full SHA.
3. Dispatch `deploy-preview.yml` in `gitmaruneko/yuban-preview` with `source_ref` set to that SHA.
4. Wait for the workflow to complete successfully.
5. Verify `preview-ref.txt`, `preview-version.txt`, and the preview page.
6. Report the workflow URL, source ref, source SHA, and verification result.

Requirements
- GitHub CLI (`gh`) must be installed and authenticated.
- The source commit must already be pushed to `gitmaruneko/yuban`.
- Do not use force-push or modify the preview repository source as part of this skill.

Examples

```powershell
./tools/deploy_preview/deploy-preview.ps1 `
  -SourceRef feature/refresh-learning-materials-page `
  -ExpectedText "中秋節任務（學齡前）"
```

Safety
- Ask for confirmation before deploying when the user has not explicitly requested a preview deployment.
- Never report success from the workflow alone; verify the deployed marker files and requested page content.
- Do not expose GitHub tokens or credentials in output.
- A successful preview deployment does not mean the production site has been deployed. Production remains controlled by the `main` workflow.
