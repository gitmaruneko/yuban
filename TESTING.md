# 育伴測試指南

保護父母尋找可信資源、查看詳情、提交／回報與下載學習素材的主要流程。功能需求參考 [PRD](docs/PRD.md) 與 [網站說明](website/README.md)；若需求與實作不一致，先確認預期行為，再決定測試結果。

## 執行測試

在專案根目錄執行。需備妥 Python、支援 `node --test` 的 Node.js，首次使用先安裝依賴：

```sh
python -m pip install -r requirements.txt
```

全部自動檢查，也可透過 VS Code 的 `Run All Tests` 工作執行：

```sh
python -m unittest discover -s tests -v
node --test tests/search-utils.test.mjs
python tools/validate_resources.py
```

[PR 檢查工作流程](.github/workflows/pr-checks.yml) 會在 Pull Request targeting `main` 時執行這三項檢查，作為合併條件。[部署工作流程](.github/workflows/deploy-pages.yml) 在 Pull Request 合併至 `main` 或手動觸發時再次執行相同檢查，成功後才部署 `website/`。目前沒有網站編譯步驟或瀏覽器 E2E 測試。

## 依變更選擇驗證

| 變更範圍 | 應做的檢查 | 現有測試／工具 |
| --- | --- | --- |
| 資源資料、欄位或匯入 | 驗證必填欄位、分類、來源與網址、重複 ID／URL；修改匯入邏輯時補上轉換或合併測試。 | `tools/validate_resources.py`、`tests/test_validate_resources.py`、`tests/test_import_resources.py` |
| 搜尋、篩選或分批顯示 | 測試受影響的正常、空結果與邊界情況，包含多條件篩選、全齡／全國資源、舊資料預設值及載入更多。 | `tests/search-utils.test.mjs` |
| 學習素材或下載連結 | 檢查本地檔案及下載連結；抽查新增或替換的 PNG、PDF、ZIP 可開啟且內容正確。僅檢查實際提供的格式。 | `tests/test_learning_materials.py` |
| 贊助設定、樣式或互動 | 執行相關回歸測試，並在瀏覽器確認受影響畫面與操作。 | `tests/test_support_config.py`、`tests/test_website_styles.py` |
| 純文件、文案或格式 | 核對內容、連結；影響網頁排版時預覽該頁。通常不需新增測試或跑完整套件。 | 人工檢查 |

欄位與允許值參考 [資源模板](docs/resource-template.md) 及驗證器，本文件不重複定義 schema。資料契約改變時，同步更新受影響的匯入、前端、驗證與測試。新增或修改資源內容時，抽查摘要、分類與原始來源一致；標示「人工核實」需有實際人工核實依據，資料驗證通過不能取代內容審核。

現有自動測試有以下限制：搜尋測試未涵蓋 Fuse 搜尋路徑；匯入測試僅涵蓋資料列轉換與合併，未涵蓋完整工作簿讀寫／歸檔；素材測試檢查路徑與下載屬性，不驗證檔案內容；樣式測試檢查 CSS 文字，不驗證實際畫面。修改這些未覆蓋部分時，補上相應的人工或自動驗證；工作簿讀寫驗證使用暫存副本。

## 瀏覽器檢查

本地預覽請使用靜態伺服器，讓 JSON 能正常載入：

```sh
python -m http.server 8000 --directory website
```

開啟 `http://localhost:8000/`，依變更選擇下列流程。版面、導覽或控制項變更需確認桌面與手機寬度，並檢查鍵盤操作、焦點與輸入標籤。

| 流程 | 檢查重點 |
| --- | --- |
| 首頁、搜尋與篩選 | 導覽連結可用；搜尋與篩選能合併使用；結果、計數、清除條件及載入更多正確；無結果與載入失敗有提示。修改搜尋時，同時確認 Fuse 正常載入及載入失敗時的基本搜尋。 |
| 資源詳情 | 標題、摘要、來源、審核標示、注意事項與原始連結正確；缺少／不存在的 ID 或資料載入失敗有錯誤提示。 |
| 提交與問題回報 | 回報帶入正確資源；必填與 HTTP(S) 網址驗證有效；GitHub Issue 預填標題與內容正確，公開提案與隱私提醒清楚。驗證預填內容即可，不實際建立測試 Issue。 |
| 學習素材 | 從首頁可前往素材頁；下載連結對應正確檔案，新增或替換的素材能開啟。 |
| 贊助區 | 顯示狀態、收款方式與 QR 圖片符合設定；不需實際付款。 |

外部連結測試檢查網址與呈現，不依賴第三方網站即時可用；自有下載檔案缺失則必須修正。

## 測試與交付原則

- 沿用 Python unittest 與 Node test，測試可觀察行為，使用小且獨立的資料。修 bug 時加入能重現缺陷的回歸測試；若不適合自動化，記錄重現與人工驗證方式。
- 依風險與維護成本決定是否新增整合／瀏覽器測試。不設覆蓋率百分比，不要求每項功能都補齊各層測試，也不預先建立 E2E 基礎設施。
- 開發與交付時完成受影響的檢查；涉及共用邏輯、資料契約或部署設定時，執行三項完整自動檢查。不要停用測試或弱化斷言來掩蓋失敗；需求改變時同步更新測試。
- 交付時說明執行結果、未執行項目及原因，區分自動測試與瀏覽器驗證。其他工程原則遵循 [engineering-standards](.agents/skills/engineering-standards/SKILL.md)。
