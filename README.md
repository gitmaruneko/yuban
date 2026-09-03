# YuBan 育伴

Helping parents find trustworthy knowledge and practical tools for raising children.

---

## 部署

本專案已設定 GitHub Actions 來自動部署 GitHub Pages。

每次推送到 `main` 分支時，工作流程會自動將 `website` 資料夾上傳為網站產物，並部署至 GitHub Pages。

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

測試涵蓋資源資料驗證，以及首頁搜尋與篩選的核心規則。GitHub Pages 部署前也會自動執行相同檢查。

### 新增育兒資源

將新資源依照 `docs/resource-template.csv` 的欄位格式填入 Excel 工作簿，再在專案根目錄執行：

```bash
python tools/import_resources.py
python tools/validate_resources.py
```

匯入程式會將 Excel 資料追加到既有網站索引；相同網址或 ID 的資源會自動跳過，不會重複加入。完成檢查後提交 `website/data/sample-resources.json`，推送到 `main` 才會發布更新。

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

1. 將變更加入 git：
   ```bash
   git add .
   ```
2. 建立提交：
   ```bash
   git commit -m "feat: ..."
   ```
3. 推送至遠端：
   ```bash
   git push origin main
   ```

GitHub Actions 會自動接管部署流程，並將 `website` 資料夾部署至 GitHub Pages。

---

### AI 開發

This project uses Matt Pocock Skills for AI-assisted development.

To update skills:

```bash
npx skills@latest update
```
