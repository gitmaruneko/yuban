# YuBan 育伴

Helping parents find trustworthy knowledge and practical tools for raising children.

[![GitHub Pages 部署狀態](https://github.com/gitmaruneko/yuban/actions/workflows/deploy-pages.yml/badge.svg?branch=main)](https://github.com/gitmaruneko/yuban/actions/workflows/deploy-pages.yml)

[前往 YuBan 正式網站](https://gitmaruneko.github.io/yuban/)

## 專案快照

資料統計（2026-09-09）：**101** 筆資源、**96** 筆人工核實資源、**46** 個主題分類。

- 資源資料經欄位、分類與重複網址驗證後才會納入網站索引。
- [開發歷程](docs/HISTORY.md) 記錄重要功能、資源與工作流程的演進。
- 部署 badge 顯示 `main` 最新 GitHub Actions 部署流程的結果；正式網站可直接由上方連結開啟。

---

## 部署

本專案已設定 GitHub Actions 來自動部署 GitHub Pages。

Pull Request 合併到 `main` 後，工作流程會再次執行完整檢查，將 `website` 資料夾上傳為網站產物，並部署至 GitHub Pages。

目前部署網址：

https://gitmaruneko.github.io/yuban/

---

## 開發流程

### 測試

最方便的方式是在 VS Code 按 `Ctrl+Shift+B`，選擇或執行預設的 `Run All Tests` 工作。也可以開啟命令面板（`Ctrl+Shift+P`），執行 `Tasks: Run Task`，再選擇 `Run All Tests`。

在專案根目錄執行全部測試：

```bash
python -m unittest discover -s tests -v
node --test tests/search-utils.test.mjs
python tools/validate_resources.py
```

測試涵蓋資源資料驗證，以及首頁搜尋與篩選的核心規則。對 `main` 建立 Pull Request 及 GitHub Pages 部署前，都會自動執行相同檢查。

### 新增育兒資源

將新資源依照 `docs/resource-template.csv` 的欄位格式填入 Excel 工作簿，放在 `docs/` 後，在專案根目錄執行：

```bash
python tools/import_resources.py --input docs/你的新資源.xlsx
python tools/validate_resources.py
```

匯入成功後，來源 Excel 會歸檔至 `docs/imported-resources/`，完整累積資料會產生在 `docs/resource_total.xlsx`。相同網址或 ID 的資源會自動跳過，不會重複加入；若省略 `--input`，則會以 `docs/resource_total.xlsx` 作為輸入。

資源模板另外提供年齡群組、地區、資源類型、使用對象、來源地區與語言欄位。地區可填入全國、縣市或鄉鎮名稱；多個值請以逗號分隔。既有索引資料會由網站以相容預設值載入，之後可逐筆補齊分類。

### 本地開發

1. 進入專案根目錄：
   ```bash
   cd yuban
   ```
2. 開啟本地靜態預覽
   - 直接用瀏覽器打開 `website/index.html`。
   - 或使用簡單的本地靜態伺服器，例如：
     ```bash
     npx serve website
     ```

### 推送與部署

1. 從最新的 `main` 建立短期分支：
   ```bash
   git switch main
   git pull
   git switch -c feature/主題
   ```
   修正問題時使用 `fix/主題`。
2. 將變更加入 git 並建立提交：
   ```bash
   git add .
   git commit -m "feat: ..."
   ```
3. 推送短期分支：
   ```bash
   git push -u origin feature/主題
   ```
4. 需要遠端預覽時，到 [yuban-preview Actions](https://github.com/gitmaruneko/yuban-preview/actions/workflows/deploy-preview.yml) 手動執行 `Deploy preview`，在 `source_ref` 輸入完整分支名稱。完成後開啟 https://gitmaruneko.github.io/yuban-preview/ 檢查結果。
5. 從短期分支建立 targeting `main` 的 Pull Request，等待 `PR checks / test` 通過後合併。
6. 合併後刪除短期分支。

Pull Request 合併後，GitHub Actions 會在 `main` 再次執行完整檢查，成功才將 `website` 資料夾部署至正式 GitHub Pages。不要直接推送 `main`。

---

### AI 開發

This project uses Matt Pocock Skills for AI-assisted development.

To update skills:

```bash
npx skills@latest update
```
