import unittest
from pathlib import Path


STYLES_PATH = Path(__file__).parents[1] / "website" / "styles.css"


class WebsiteStyleRegressionTests(unittest.TestCase):
    def test_resource_list_item_contains_expanded_title_link(self):
        styles = STYLES_PATH.read_text(encoding="utf-8")

        self.assertIn(
            ".resource-list-item {\n  position: relative;",
            styles,
        )
        self.assertIn(
            ".resource-title a::after {\n  position: absolute;",
            styles,
        )


if __name__ == "__main__":
    unittest.main()