const ISSUE_URL = "https://github.com/gitmaruneko/yuban/issues/new";

function setReportMode(params) {
  const isReport = params.get("mode") === "report";
  if (!isReport) return;

  document.querySelector("#submissionMode").value = "report";
  document.querySelector("#breadcrumbLabel").textContent = "回報資源問題";
  document.querySelector("#pageTitle").textContent = "回報連結或內容問題";
  document.querySelector("#pageDescription").textContent =
    "告訴我們失效連結、內容更新或分類問題。送出後會前往 GitHub 建立公開回報。";
  document.querySelector("#reasonLabel").textContent = "發現什麼問題？ ＊";
  document.querySelector("#submissionReason").placeholder =
    "例如：連結失效、內容已改版、摘要與原文不符，或適用年齡需要調整。";
  document.querySelector("#submitButton").textContent = "前往 GitHub 送出回報";
  document.querySelector("#resourceTitle").value = params.get("title") || "";
  document.querySelector("#resourceUrl").value = params.get("url") || "";
  document.title = "回報資源問題｜育伴 YuBan";
}

function buildIssue(formData, mode) {
  const title = formData.get("title").trim();
  const resourceUrl = formData.get("url").trim();
  const age = formData.get("age");
  const type = formData.get("type");
  const reason = formData.get("reason").trim();
  const isReport = mode === "report";

  const issueTitle = isReport ? `[資源回報] ${title}` : `[資源推薦] ${title}`;
  const body = [
    `## ${isReport ? "問題資源" : "推薦資源"}`,
    "",
    `- 資源名稱：${title}`,
    `- 原始網址：${resourceUrl}`,
    `- 適用年齡：${age}`,
    `- 內容類型：${type}`,
    "",
    `## ${isReport ? "問題說明" : "推薦原因"}`,
    "",
    reason,
    "",
    "---",
    "由育伴 MVP 網站表單產生。請勿在公開 Issue 留下個人敏感資訊。",
  ].join("\n");

  const issueParams = new URLSearchParams({ title: issueTitle, body });
  return `${ISSUE_URL}?${issueParams.toString()}`;
}

(function initializeSubmissionForm() {
  const params = new URLSearchParams(window.location.search);
  const form = document.querySelector("#submissionForm");
  const status = document.querySelector("#formStatus");
  setReportMode(params);

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    status.textContent = "";

    if (!form.reportValidity()) return;

    const formData = new FormData(form);
    const resourceUrl = formData.get("url").trim();
    try {
      const parsedUrl = new URL(resourceUrl);
      if (!['http:', 'https:'].includes(parsedUrl.protocol)) throw new Error("Unsupported URL");
    } catch (error) {
      document.querySelector("#resourceUrl").setCustomValidity("請輸入有效的 http 或 https 網址");
      document.querySelector("#resourceUrl").reportValidity();
      return;
    }

    document.querySelector("#resourceUrl").setCustomValidity("");
    const mode = document.querySelector("#submissionMode").value;
    status.textContent = "正在前往 GitHub；你仍可在送出前修改內容。";
    window.location.assign(buildIssue(formData, mode));
  });

  document.querySelector("#resourceUrl").addEventListener("input", (event) => {
    event.currentTarget.setCustomValidity("");
  });
})();
