import copy
import json
import unittest
from pathlib import Path

from tools.import_resources import convert_row, merge_resources


RESOURCE_PATH = Path(__file__).parents[1] / "website" / "data" / "sample-resources.json"


class MergeResourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources = json.loads(RESOURCE_PATH.read_text(encoding="utf-8"))

    def test_skips_existing_resource_and_appends_new_resource(self):
        existing = self.resources[:1]
        duplicate = copy.deepcopy(existing[0])
        new_resource = copy.deepcopy(existing[0])
        new_resource["id"] = "resource-new"
        new_resource["url"] = "https://example.com/new"
        new_resource["source"]["url"] = new_resource["url"]

        merged, skipped = merge_resources(existing, [duplicate, new_resource])

        self.assertEqual(skipped, 1)
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[-1]["url"], "https://example.com/new")


class ConvertResourceTests(unittest.TestCase):
    def test_converts_explicit_taxonomy_fields(self):
        row = {
            "資源名稱": "測試資源",
            "連結": "https://example.com/resource",
            "摘要": "測試摘要",
            "內容類型": "電子手冊",
            "提供方／來源類型": "政府",
            "原始來源": "測試政府",
            "是否為入口型資源": "否",
            "年齡階段": "全齡",
            "主題": "健康與生活照護",
            "關鍵標籤": "睡眠, 作息",
            "審核狀態": "人工核實",
            "可信度備註": "測試備註",
            "注意事項": "測試提醒",
            "年齡群組": "國小, 國中",
            "地區": "新北市, 板橋區",
            "資源類型": "政策",
            "使用對象": "家長, 教師",
            "來源地區": "日本",
            "語言": "日文, 繁體中文",
        }

        resource = convert_row(row, 2)

        self.assertEqual(resource["age_groups"], ["國小", "國中"])
        self.assertEqual(resource["regions"], ["新北市", "板橋區"])
        self.assertEqual(resource["resource_categories"], ["政策"])
        self.assertEqual(resource["audiences"], ["家長", "教師"])
        self.assertEqual(resource["origin_region"], "日本")
        self.assertEqual(resource["languages"], ["日文", "繁體中文"])


if __name__ == "__main__":
    unittest.main()