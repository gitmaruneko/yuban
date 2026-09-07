---
description: "Review changes, run relevant checks, create an English Conventional Commit, and push it to the current remote branch"
name: "Commit and Push"
argument-hint: "Optional commit intent or scope"
agent: "agent"
---

請依照以下流程完成本次提交與推送：

1. 檢查工作區狀態、目前分支、遠端同步狀態與待提交差異。
2. 只納入與本次任務相關的檔案；不要自動加入無關、敏感或未確認的檔案。
3. 依照專案既有設定執行最相關的測試、驗證或 lint。測試失敗時不得提交，先修正問題或回報阻塞原因。
4. 建立英文 commit message，遵循 Conventional Commits 1.0.0：

   ```text
   <type>(<scope>): <imperative description>
   ```

   - `type` 只能使用適合此次變更的標準類型，例如 `feat`、`fix`、`docs`、`refactor`、`test`、`build`、`ci`、`chore`。
   - `scope` 可省略；若使用，請填寫受影響的模組或領域。
   - description 必須是英文、祈使語氣、簡潔明確，不以句號結尾。
   - commit message 的 subject、body、footer 全部只能使用英文。
   - 需要 breaking change 時，使用 `!` 或英文 `BREAKING CHANGE:` footer，並清楚說明影響。
   - 不要使用模糊訊息，例如 `update`、`fix stuff`、`changes` 或 `commit changes`。

   合法範例：

   ```text
   fix(submission): preserve navigation button text color
   feat(search): add language and region filters
   docs: document resource import workflow
   ```

5. 建立 commit 後確認 commit message 與變更內容正確，再執行 `git push` 到目前分支的 upstream remote。
6. 若沒有 upstream，先確認遠端與目標分支；不要猜測或推送到其他分支。
7. 最後回報：測試結果、commit hash、commit message、推送結果，以及仍未提交的檔案。所有 Git commit message 必須維持英文，即使回報內容使用中文。

如果使用者提供了額外的 commit intent 或 scope，請在不違反上述規則的前提下採用；若與實際 diff 不一致，以實際變更為準。
