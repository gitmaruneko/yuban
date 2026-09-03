import json
import unittest
from pathlib import Path


CONFIG_PATH = Path(__file__).parents[1] / "website" / "data" / "support-config.json"


class SupportConfigTests(unittest.TestCase):
    def test_support_is_enabled_with_the_streetpay_qr_code(self):
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

        self.assertTrue(config["enabled"])
        self.assertEqual({provider["id"] for provider in config["providers"]}, {"streetpay", "linepay"})
        streetpay = next(provider for provider in config["providers"] if provider["id"] == "streetpay")
        linepay = next(provider for provider in config["providers"] if provider["id"] == "linepay")
        self.assertTrue(streetpay["enabled"])
        self.assertEqual(streetpay["qr_code_url"], "assets/streetpay-qr.jpg")
        self.assertTrue(streetpay["qr_code_url"].endswith("streetpay-qr.jpg"))
        self.assertFalse(linepay["enabled"])
        self.assertFalse(linepay["qr_code_url"])


if __name__ == "__main__":
    unittest.main()