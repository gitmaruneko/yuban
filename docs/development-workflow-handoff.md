# 開發流程調整交接

## 目標

單人開發從最新 `main` 建立短期 `feature/*` 或 `fix/*` 分支，使用共用 `yuban-preview` 遠端預覽，再由短期分支建立 Pull Request 到 `main`。PR 自動檢查通過後才合併，正式站在 `main` 再次通過完整檢查後部署。

## 遠端分支

| Repository | Branch | 用途 |
| --- | --- | --- |
| `gitmaruneko/yuban-preview` | `feature/source-ref-preview` | 讓預覽 workflow 手動接受 `yuban` 的來源分支或 commit |
| `gitmaruneko/yuban` | `feature/pr-preview-workflow` | 新增 PR checks 並記錄短期分支交付流程 |

## 接續順序

1. 先在 `yuban-preview` 建立 `feature/source-ref-preview` targeting `main` 的 PR，確認變更後合併。`workflow_dispatch` 必須先存在於 default branch，Actions 頁面才會提供 `source_ref` 輸入。
2. 在 `yuban-preview` 的 Actions → Deploy preview → Run workflow 輸入 `feature/pr-preview-workflow`。
3. 確認 https://gitmaruneko.github.io/yuban-preview/ 顯示正確分支與 commit，並檢查 `preview-ref.txt`、`preview-version.txt`。
4. 在 `yuban` 建立 `feature/pr-preview-workflow` targeting `main` 的 PR，確認 `PR checks / test` 成功後合併。
5. 等待 `Deploy site to GitHub Pages` 在 `main` 重跑測試並部署 https://gitmaruneko.github.io/yuban/ 。
6. 在 `yuban` repository settings 建立 `main` ruleset：要求 Pull Request、禁止直接 push，並要求 `PR checks / test` 成功。單人 repository 不必強制其他 reviewer approval。
7. 刪除兩個已合併的遠端 feature 分支。確認舊 `develop` 沒有其他待保留內容後，再決定是否刪除；本次變更不會自動刪除它。

## 另一台電腦接續

若 repository 尚未 clone：

```bash
git clone https://github.com/gitmaruneko/yuban.git
git clone https://github.com/gitmaruneko/yuban-preview.git
```

若已經存在本機：

```bash
git -C yuban fetch origin
git -C yuban switch --track origin/feature/pr-preview-workflow

git -C yuban-preview fetch origin
git -C yuban-preview switch --track origin/feature/source-ref-preview
```

若本機已經有同名 branch，改用 `git switch <branch>` 後執行 `git pull --ff-only`。

## 已完成驗證

- `python -m unittest discover -s tests -v`：16 項通過。
- `node --test tests/search-utils.test.mjs`：9 項通過。
- `python tools/validate_resources.py`：64 筆資源通過。
- 兩個 repository 的 `git diff --check` 通過。
- VS Code 對兩份 workflow 與相關 Markdown 未回報 diagnostics。
- 本機未安裝 `actionlint`，因此尚未執行該工具。

## 尚待完成

- 建立並合併兩個 Pull Request。
- 實際執行一次手動 preview deployment 與頁面檢查。
- 設定 `main` ruleset。GitHub CLI 在原電腦尚未登入，因此 repository-hosted 設定未執行。