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
