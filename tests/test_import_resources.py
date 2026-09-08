import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.import_resources import (
    archive_input,
    convert_row,
    exclude_authorized_duplicate_urls,
    merge_resources,
)


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

    def test_rejects_existing_url_unless_explicitly_excluded(self):
        existing = [{"url": "https://example.com/existing"}]
        incoming = [
            {"url": "https://example.com/existing"},
            {"url": "https://example.com/new"},
        ]

        with self.assertRaisesRegex(ValueError, "already in the resource index"):
            exclude_authorized_duplicate_urls(incoming, existing, set())

        filtered, excluded = exclude_authorized_duplicate_urls(
            incoming, existing, {"https://example.com/existing"}
        )

        self.assertEqual(excluded, ["https://example.com/existing"])
        self.assertEqual(filtered, [{"url": "https://example.com/new"}])

    def test_moves_source_to_archive_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "resource.xlsx"
            archive_dir = root / "archive"
            source.write_text("workbook placeholder", encoding="utf-8")

            archived = archive_input(source, archive_dir)

            self.assertEqual(archived, archive_dir / source.name)
            self.assertFalse(source.exists())
            self.assertEqual(archived.read_text(encoding="utf-8"), "workbook placeholder")

    def test_refuses_to_replace_an_existing_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "resource.xlsx"
            archive_dir = root / "archive"
            archive_dir.mkdir()
            source.write_text("new source", encoding="utf-8")
            (archive_dir / source.name).write_text("existing archive", encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "Archive already exists"):
                archive_input(source, archive_dir)

            self.assertEqual(source.read_text(encoding="utf-8"), "new source")


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

    def test_converts_preconception_stage_and_reproductive_topic(self):
        row = {
            "資源名稱": "備孕測試資源",
            "連結": "https://example.com/preconception",
            "摘要": "測試備孕分類",
            "內容類型": "文章",
            "提供方／來源類型": "政府",
            "原始來源": "測試政府",
            "是否為入口型資源": "否",
            "年齡階段": "備孕",
            "主題": "備孕與生殖",
            "關鍵標籤": "人工受孕, 不孕症, IVF, 生殖醫療",
            "審核狀態": "人工核實",
            "可信度備註": "測試備註",
            "注意事項": "測試提醒",
            "年齡群組": "全齡",
            "地區": "全國",
            "資源類型": "學習教材",
            "使用對象": "家長",
            "來源地區": "台灣",
            "語言": "繁體中文",
        }

        resource = convert_row(row, 2)

        self.assertEqual(resource["age_ranges"], ["備孕"])
        self.assertEqual(resource["topic_group"], "健康與照護")
        self.assertEqual(resource["tags"], ["人工受孕", "不孕症", "IVF", "生殖醫療"])

    def test_converts_reviewed_health_need_aliases_to_compact_topics(self):
        base_row = {
            "資源名稱": "健康需求測試資源",
            "連結": "https://example.com/health-need",
            "摘要": "測試工作簿別名轉換",
            "內容類型": "官方QA",
            "提供方／來源類型": "政府",
            "原始來源": "測試政府",
            "是否為入口型資源": "否",
            "關鍵標籤": "測試標籤",
            "審核狀態": "通過",
            "可信度備註": "測試依據",
            "注意事項": "測試提醒",
            "年齡群組": "全齡",
            "地區": "全國",
            "資源類型": "指南型",
            "使用對象": "家長",
            "來源地區": "台灣",
            "語言": "繁體中文",
        }
        cases = [
            ("高齡妊娠", "孕期", "孕產與嬰幼兒照護", ["孕期"]),
            ("人工受孕", "備孕／不孕療程", "備孕與生殖", ["備孕"]),
            ("唇顎裂", "新生兒至青少年", "兒科疾病與照護", ["0-1歲", "1-3歲", "3-6歲"]),
            ("早療", "嬰幼兒／學齡前", "發展與早療", ["0-1歲", "1-3歲", "3-6歲"]),
            ("ADHD", "全齡", "注意力與過動（ADHD）", ["全齡"]),
        ]

        for index, (raw_topic, age_label, expected_topic, expected_ages) in enumerate(cases):
            with self.subTest(raw_topic=raw_topic):
                row = {
                    **base_row,
                    "連結": f"https://example.com/health-need-{index}",
                    "主題": raw_topic,
                    "年齡階段": age_label,
                }

                resource = convert_row(row, index + 2)

                self.assertEqual(resource["type"], "文章")
                self.assertEqual(resource["topic"], expected_topic)
                self.assertEqual(resource["age_ranges"], expected_ages)

    def test_converts_adhd_school_age_resource_without_broadening_to_toddlers(self):
        row = {
            "資源名稱": "ADHD 校園支持",
            "連結": "https://example.com/adhd-school-support",
            "摘要": "提供 ADHD 學校支持資訊。",
            "內容類型": "教育權益說明",
            "提供方／來源類型": "政府",
            "原始來源": "測試教育局",
            "是否為入口型資源": "否",
            "年齡階段": "學齡兒童／青少年",
            "主題": "ADHD",
            "關鍵標籤": "ADHD, 校園支持",
            "審核狀態": "通過",
            "可信度備註": "測試依據",
            "注意事項": "測試提醒",
            "年齡群組": "6–18歲",
            "地區": "全國",
            "資源類型": "教育權益型",
            "使用對象": "家長／教師／青少年",
            "來源地區": "台灣",
            "語言": "繁體中文",
        }

        resource = convert_row(row, 2)

        self.assertEqual(resource["type"], "文章")
        self.assertEqual(resource["topic"], "注意力與過動（ADHD）")
        self.assertEqual(resource["age_ranges"], ["國小", "國中", "高中"])
        self.assertEqual(resource["age_groups"], ["國小", "國中", "高中"])
        self.assertEqual(resource["audiences"], ["家長", "教師", "兒童"])


if __name__ == "__main__":
    unittest.main()
