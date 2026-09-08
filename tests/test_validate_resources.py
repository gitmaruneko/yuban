import copy
import json
import unittest
from pathlib import Path

from tools.validate_resources import validate_resources


RESOURCE_PATH = Path(__file__).parents[1] / "website" / "data" / "sample-resources.json"


class ValidateResourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources = json.loads(RESOURCE_PATH.read_text(encoding="utf-8"))

    def test_sample_resources_are_valid(self):
        validate_resources(self.resources)

    def test_accepts_fewer_than_thirty_resources(self):
        resources = self.resources[:-1]
        validate_resources(resources)

    def test_accepts_more_than_mvp_resource_count(self):
        resources = copy.deepcopy(self.resources)
        resources.append(copy.deepcopy(resources[0]))
        resources[-1]["id"] = "resource-new"
        resources[-1]["url"] = "https://example.com/new"
        resources[-1]["source"]["url"] = resources[-1]["url"]

        validate_resources(resources)

    def test_rejects_duplicate_resource_id(self):
        resources = copy.deepcopy(self.resources)
        resources[1]["id"] = resources[0]["id"]

        with self.assertRaisesRegex(ValueError, "Duplicate resource ID"):
            validate_resources(resources)

    def test_rejects_duplicate_resource_url(self):
        resources = copy.deepcopy(self.resources)
        resources[1]["url"] = resources[0]["url"]

        with self.assertRaisesRegex(ValueError, "Duplicate resource URL"):
            validate_resources(resources)

    def test_rejects_unsupported_review_status(self):
        resources = copy.deepcopy(self.resources)
        resources[0]["ai_summary_status"] = "pending"

        with self.assertRaisesRegex(ValueError, "unsupported review status"):
            validate_resources(resources)

    def test_rejects_unsupported_age_stage(self):
        resources = copy.deepcopy(self.resources)
        resources[0]["age_ranges"] = ["7-9歲"]

        with self.assertRaisesRegex(ValueError, "unsupported age stages"):
            validate_resources(resources)

    def test_accepts_new_health_and_early_support_taxonomy(self):
        resources = []
        cases = [
            ("備孕與生殖", "健康與照護", ["備孕"], ["人工受孕", "不孕症", "IVF", "生殖醫療"]),
            ("孕期健康", "健康與照護", ["孕期"], ["高齡妊娠", "產前檢查", "高風險妊娠"]),
            ("兒童健康與醫療", "健康與照護", ["0-1歲", "1-3歲", "3-6歲"], ["唇顎裂", "兔唇", "顎裂", "先天性疾病"]),
            ("發展與早期支持", "發展與學習", ["0-1歲", "1-3歲", "3-6歲"], ["早療", "發展遲緩", "聯合評估", "療育"]),
        ]
        for index, (topic, topic_group, age_ranges, tags) in enumerate(cases):
            resource = copy.deepcopy(self.resources[0])
            resource["id"] = f"resource-taxonomy-{index}"
            resource["url"] = f"https://example.com/taxonomy-{index}"
            resource["source"]["url"] = resource["url"]
            resource["topic"] = topic
            resource["topic_group"] = topic_group
            resource["age_ranges"] = age_ranges
            resource["tags"] = tags
            resources.append(resource)

        validate_resources(resources)

    def test_rejects_unsupported_topic_and_mismatched_topic_group(self):
        resources = copy.deepcopy(self.resources)
        resources[0]["topic"] = "人工受孕"

        with self.assertRaisesRegex(ValueError, "unsupported topic"):
            validate_resources(resources)

        resources[0]["topic"] = "孕期健康"
        resources[0]["topic_group"] = "發展與學習"
        with self.assertRaisesRegex(ValueError, "topic group must be 健康與照護"):
            validate_resources(resources)

    def test_rejects_unsupported_resource_category(self):
        resources = copy.deepcopy(self.resources)
        resources[0]["resource_categories"] = ["未定義類型"]

        with self.assertRaisesRegex(ValueError, "unsupported resource_categories"):
            validate_resources(resources)

    def test_rejects_non_array_taxonomy_field(self):
        resources = copy.deepcopy(self.resources)
        resources[0]["languages"] = "繁體中文"

        with self.assertRaisesRegex(ValueError, "languages must be a non-empty string array"):
            validate_resources(resources)


if __name__ == "__main__":
    unittest.main()
