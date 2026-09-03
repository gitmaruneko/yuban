import { filterResources, searchResources } from "./search-utils.mjs";

const RESOURCE_DATA_URL = "data/sample-resources.json";
const FUSE_MODULE_URL = "https://cdn.jsdelivr.net/npm/fuse.js@7.5.0/dist/fuse.min.mjs";

const collator = new Intl.Collator("zh-Hant");
let FuseSearch = null;

function createElement(tagName, className, text) {
  const element = document.createElement(tagName);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function getStatus(resource) {
  const verified = resource.ai_summary_status === "verified";
  return {
    label: verified ? "人工核實" : "AI 整理・待人工核實",
    className: verified ? "verified" : "draft",
  };
}

function appendMetaItem(list, label, value) {
  const item = createElement("div", "resource-meta-item");
  item.append(createElement("dt", "", label), createElement("dd", "", value));
  list.append(item);
}

function renderResourceCard(resource) {
  const article = createElement("article", "resource-card");
  const top = createElement("div", "resource-card-top");
  const topic = createElement("span", "topic-label", resource.topic_group);
  const status = getStatus(resource);
  const statusBadge = createElement("span", `status-badge ${status.className}`, status.label);
  top.append(topic, statusBadge);

  const title = createElement("h3", "resource-title");
  const titleLink = createElement("a", "", resource.title);
  titleLink.href = `resource.html?id=${encodeURIComponent(resource.id)}`;
  title.append(titleLink);

  const summary = createElement("p", "resource-summary", resource.summary);
  const meta = createElement("dl", "resource-meta");
  appendMetaItem(meta, "適用", resource.age_label);
  appendMetaItem(meta, "來源", resource.source.name);
  appendMetaItem(meta, "形式", resource.type_label);

  const tags = createElement("ul", "tag-list");
  tags.setAttribute("aria-label", "關鍵標籤");
  resource.tags.slice(0, 4).forEach((tag) => {
    tags.append(createElement("li", "", tag));
  });

  const footer = createElement("div", "resource-card-footer");
  const sourceType = createElement("span", "source-type", resource.source.type);
  const detailLink = createElement("a", "detail-link", "查看育伴詳情");
  detailLink.href = `resource.html?id=${encodeURIComponent(resource.id)}`;
  detailLink.setAttribute("aria-label", `查看「${resource.title}」的育伴詳情`);
  footer.append(sourceType, detailLink);

  article.append(top, title, summary, meta, tags, footer);
  return article;
}

function populateSelect(select, values) {
  [...new Set(values)].sort(collator.compare).forEach((value) => {
    const option = createElement("option", "", value);
    option.value = value;
    select.append(option);
  });
}

function debounce(callback, delay) {
  let timeoutId;
  return (...args) => {
    window.clearTimeout(timeoutId);
    timeoutId = window.setTimeout(() => callback(...args), delay);
  };
}

async function loadResources() {
  const response = await fetch(RESOURCE_DATA_URL);
  if (!response.ok) throw new Error(`Resource request failed: ${response.status}`);
  const resources = await response.json();
  if (!Array.isArray(resources)) throw new Error("Resource data is not an array");
  return resources;
}

async function loadSearchEngine() {
  try {
    const fuseModule = await import(FUSE_MODULE_URL);
    FuseSearch = fuseModule.default;
  } catch (error) {
    console.warn("Fuse.js could not be loaded; using basic keyword matching.", error);
  }
}

(async function initializeSearch() {
  const form = document.querySelector("#searchForm");
  const queryInput = document.querySelector("#q");
  const topicSelect = document.querySelector("#topic-filter");
  const sourceSelect = document.querySelector("#source-filter");
  const typeSelect = document.querySelector("#type-filter");
  const resetButton = document.querySelector("#resetFilters");
  const moreFilters = document.querySelector("#moreFilters");
  const filterCount = document.querySelector("#filterCount");
  const resultsGrid = document.querySelector("#resultsGrid");
  const resultsSummary = document.querySelector("#resultsSummary");
  const loadError = document.querySelector("#loadError");
  const searchEngineNote = document.querySelector("#searchEngineNote");

  let resources;
  try {
    [resources] = await Promise.all([loadResources(), loadSearchEngine()]);
  } catch (error) {
    console.error(error);
    resultsGrid.replaceChildren();
    resultsGrid.setAttribute("aria-busy", "false");
    resultsGrid.hidden = true;
    loadError.hidden = false;
    resultsSummary.textContent = "資源載入失敗";
    return;
  }

  populateSelect(topicSelect, resources.map((resource) => resource.topic));
  populateSelect(sourceSelect, resources.map((resource) => resource.source.type));
  populateSelect(typeSelect, resources.map((resource) => resource.type));

  document.querySelector("#resourceCount").textContent = resources.length;
  document.querySelector("#sourceTypeCount").textContent = new Set(
    resources.map((resource) => resource.source.type),
  ).size;
  document.querySelector("#verifiedRate").textContent = Math.round(
    (resources.filter((resource) => resource.ai_summary_status === "verified").length /
      resources.length) *
      100,
  );
  if (!FuseSearch) searchEngineNote.textContent = "使用基本關鍵字搜尋";

  const initialParams = new URLSearchParams(window.location.search);
  queryInput.value = initialParams.get("q") || "";
  topicSelect.value = initialParams.get("topic") || "";
  sourceSelect.value = initialParams.get("source") || "";
  typeSelect.value = initialParams.get("type") || "";
  const requestedAge = initialParams.get("age") || "";
  const ageRadio = form.querySelector(`input[name="age"][value="${CSS.escape(requestedAge)}"]`);
  if (ageRadio) ageRadio.checked = true;
  if (topicSelect.value || sourceSelect.value || typeSelect.value) moreFilters.open = true;

  function getState() {
    return {
      query: queryInput.value.trim(),
      age: new FormData(form).get("age") || "",
      topic: topicSelect.value,
      source: sourceSelect.value,
      type: typeSelect.value,
    };
  }

  function updateUrl(state) {
    const params = new URLSearchParams();
    if (state.query) params.set("q", state.query);
    if (state.age) params.set("age", state.age);
    if (state.topic) params.set("topic", state.topic);
    if (state.source) params.set("source", state.source);
    if (state.type) params.set("type", state.type);
    const queryString = params.toString();
    const nextUrl = `${window.location.pathname}${queryString ? `?${queryString}` : ""}#explore`;
    window.history.replaceState(null, "", nextUrl);
  }

  function renderResults() {
    const state = getState();
    const filtered = filterResources(resources, state);
    const results = searchResources(filtered, state.query, FuseSearch);

    resultsGrid.replaceChildren();
    if (results.length) {
      results.forEach((resource) => resultsGrid.append(renderResourceCard(resource)));
      resultsSummary.textContent = state.query
        ? `找到 ${results.length} 筆與「${state.query}」相關的資源`
        : `顯示 ${results.length} 筆資源`;
    } else {
      const emptyState = createElement("div", "empty-state");
      emptyState.append(
        createElement("p", "empty-symbol", "沒有符合條件的資源"),
        createElement("p", "", "試著縮短關鍵字，或清除部分篩選條件。"),
      );
      const clearButton = createElement("button", "button secondary", "清除搜尋條件");
      clearButton.type = "button";
      clearButton.addEventListener("click", resetAll);
      emptyState.append(clearButton);
      resultsGrid.append(emptyState);
      resultsSummary.textContent = "找不到符合條件的資源";
    }

    resultsGrid.setAttribute("aria-busy", "false");
    const advancedCount = [state.topic, state.source, state.type].filter(Boolean).length;
    filterCount.textContent = advancedCount;
    filterCount.hidden = advancedCount === 0;
    updateUrl(state);
  }

  function resetAll() {
    form.reset();
    moreFilters.open = false;
    renderResults();
    queryInput.focus();
  }

  const renderAfterTyping = debounce(renderResults, 180);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    renderResults();
  });
  queryInput.addEventListener("input", renderAfterTyping);
  form.querySelectorAll('input[name="age"]').forEach((radio) => {
    radio.addEventListener("change", renderResults);
  });
  [topicSelect, sourceSelect, typeSelect].forEach((select) => {
    select.addEventListener("change", renderResults);
  });
  resetButton.addEventListener("click", resetAll);

  renderResults();
})();
