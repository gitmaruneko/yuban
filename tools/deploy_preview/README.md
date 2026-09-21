# Deploy Preview

Deploys a pushed YuBan branch or commit to the shared `yuban-preview` GitHub Pages site.

## Usage

```powershell
./tools/deploy_preview/deploy-preview.ps1 `
  -SourceRef feature/refresh-learning-materials-page `
  -ExpectedText "中秋節任務（學齡前）"
```

The script:

1. Resolves a branch to the full SHA on `origin`.
2. Dispatches `gitmaruneko/yuban-preview/.github/workflows/deploy-preview.yml`.
3. Waits for the workflow to succeed.
4. Verifies the published `preview-ref.txt`, `preview-version.txt`, and optional page text.

A source branch must be pushed before deployment. This command does not commit, push, merge, or deploy production.
