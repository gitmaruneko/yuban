# 育伴 MVP 靜態網站

## 本機預覽

請透過靜態伺服器預覽，避免瀏覽器阻擋 JSON 載入：

```bash
python -m http.server 8000 --directory website
```

開啟 http://localhost:8000/。

## 資源資料

網站資料由 `docs/resource_v0.2.xlsx` 產生。更新工作簿後，在專案根目錄執行：

```bash
python tools/import_resources.py
python tools/validate_resources.py
```

匯入程式會要求 MVP 資料維持 30 筆、網址不重複，並把工作簿的詳細分類轉成 PRD 定義的網站分類。

## 頁面

- `index.html`：資源搜尋與篩選
- `resource.html?id=...`：育伴資源詳情
- `submit.html`：資源推薦與問題回報
- `learning-materials/`：可下載的學習素材
