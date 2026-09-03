import assert from "node:assert/strict";
import test from "node:test";

import { filterResources, searchResources } from "../website/search-utils.mjs";

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