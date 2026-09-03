# 育伴 MVP 靜態網站

## 本機預覽

請透過靜態伺服器預覽，避免瀏覽器阻擋 JSON 載入：

```bash
python -m http.server 8000 --directory website
```

開啟 http://localhost:8000/。

## 資源資料

網站資料由 `docs/resource_v0.2.xlsx` 產生。新增資源時，將新資料追加到工作簿後，在專案根目錄執行：

```bash
python tools/import_resources.py
python tools/validate_resources.py
```

匯入程式會將工作簿中的新資源與既有 JSON 索引比對；相同網址或 ID 的資料會跳過，不會重複加入。資源數量不限，並把工作簿的詳細分類轉成 PRD 定義的網站分類。

## 頁面

- `index.html`：資源搜尋與篩選
- `resource.html?id=...`：育伴資源詳情
- `submit.html`：資源推薦與問題回報
- `learning-materials/`：可下載的學習素材

## 贊助設定

`data/support-config.json` 管理街口支付與 LINE Pay 的贊助設定。目前已啟用街口 QR Code，網站會在首頁頁尾展示；未來可透過 `enabled` 與 provider 設定停用或切換收款方式。
