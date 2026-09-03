import copy
import json
import unittest
from pathlib import Path

from tools.import_resources import merge_resources


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


if __name__ == "__main__":
    unittest.main()