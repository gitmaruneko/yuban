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

    def test_rejects_wrong_resource_count(self):
        resources = self.resources[:-1]

        with self.assertRaisesRegex(ValueError, "Expected 30 resources"):
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


if __name__ == "__main__":
    unittest.main()