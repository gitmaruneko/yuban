import assert from "node:assert/strict";
import test from "node:test";

import {
  filterResources,
  getVisibleResources,
  normalizeResource,
  searchResources,
} from "../website/search-utils.mjs";

const resources = [
  {
    title: "寶寶睡眠指南",
    summary: "協助建立睡眠習慣",
    topic: "睡眠",
    topic_group: "生活照護",
    source: { name: "育兒醫院", type: "醫院" },
    type: "文章",
    type_label: "文章",
    tags: ["睡眠", "作息"],
    age_ranges: ["0-1歲"],
  },
  {
    title: "親子共讀影片",
    summary: "適合全家一起觀看",
    topic: "親子互動",
    topic_group: "互動",
    source: { name: "育伴頻道", type: "個人創作者" },
    type: "影片",
    type_label: "影片",
    tags: ["閱讀"],
    age_ranges: ["全齡"],
  },
];

test("空白關鍵字回傳所有資源", () => {
  assert.deepEqual(searchResources(resources, "  "), resources);
});

test("關鍵字可搜尋標題、標籤且忽略大小寫與全半形差異", () => {
  assert.deepEqual(searchResources(resources, "睡眠"), [resources[0]]);
  assert.deepEqual(searchResources(resources, "作息"), [resources[0]]);
  assert.deepEqual(searchResources(resources, "ＡＢＣ"), []);
});

test("年齡篩選會包含全齡資源", () => {
  assert.deepEqual(filterResources(resources, { age: "0-1歲" }), resources);
  assert.deepEqual(filterResources(resources, { age: "3-6歲" }), [resources[1]]);
});

test("篩選條件會同時套用主題、來源與內容類型", () => {
  assert.deepEqual(
    filterResources(resources, {
      age: "",
      topic: "睡眠",
      source: "醫院",
      type: "文章",
    }),
    [resources[0]],
  );
});

test("結果預設只顯示前 24 筆", () => {
  const manyResources = Array.from({ length: 30 }, (_, index) => ({ id: index }));

  assert.equal(getVisibleResources(manyResources).length, 24);
  assert.deepEqual(getVisibleResources(manyResources), manyResources.slice(0, 24));
});

test("載入更多會增加一批結果但不超過總數", () => {
  const manyResources = Array.from({ length: 50 }, (_, index) => ({ id: index }));

  assert.equal(getVisibleResources(manyResources, 48).length, 48);
  assert.equal(getVisibleResources(manyResources, 72).length, 50);
});

test("分類欄位可同時套用年齡、地區、資源類型、對象、來源地區與語言", () => {
  const resource = normalizeResource({
    ...resources[0],
    age_groups: ["國小"],
    regions: ["新北市"],
    resource_categories: ["政策"],
    audiences: ["家長", "教師"],
    origin_region: "日本",
    languages: ["英文"],
  });

  assert.deepEqual(
    filterResources([resource], {
      age: "國小",
      region: "新北市",
      category: "政策",
      audience: "教師",
      origin: "日本",
      language: "英文",
    }),
    [resource],
  );
  assert.deepEqual(
    filterResources([resource], { age: "國中", region: "新北市" }),
    [],
  );
});

test("舊資源缺少新分類欄位時會套用相容預設值", () => {
  const normalized = normalizeResource(resources[0]);

  assert.deepEqual(normalized.age_groups, ["學齡前"]);
  assert.deepEqual(normalized.regions, ["全國"]);
  assert.deepEqual(normalized.resource_categories, ["學習教材"]);
  assert.deepEqual(normalized.audiences, ["家長"]);
  assert.equal(normalized.origin_region, "台灣");
  assert.deepEqual(normalized.languages, ["繁體中文"]);
});