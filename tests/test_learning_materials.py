import re
import unittest
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


PROJECT_ROOT = Path(__file__).parents[1]
MATERIALS_FILES = (
    PROJECT_ROOT / "website" / "learning-materials" / "index.html",
    PROJECT_ROOT / "website" / "learning-materials" / "README.md",
    PROJECT_ROOT / "resources" / "learning-materials" / "index.html",
    PROJECT_ROOT / "resources" / "learning-materials" / "README.md",
)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        attributes = dict(attrs)
        if "href" in attributes:
            self.links.append((attributes["href"], "download" in attributes))


def is_local_link(link):
    parsed = urlsplit(link)
    return not parsed.scheme and not parsed.netloc and not link.startswith("#")


def link_target(base_path, link):
    path = unquote(urlsplit(link).path)
    return (base_path.parent / path).resolve()


class LearningMaterialsTests(unittest.TestCase):
    def html_links(self, file_path):
        parser = LinkParser()
        parser.feed(file_path.read_text(encoding="utf-8"))
        return parser.links

    def test_all_local_html_links_exist_and_are_downloadable(self):
        for file_path in MATERIALS_FILES:
            if file_path.suffix != ".html":
                continue
            for link, has_download_attribute in self.html_links(file_path):
                if not is_local_link(link):
                    continue
                with self.subTest(file=file_path, link=link):
                    self.assertTrue(link_target(file_path, link).is_file())
                    if not has_download_attribute:
                        self.assertEqual(Path(urlsplit(link).path).suffix, ".html")

    def test_download_assets_have_expected_file_signatures(self):
        signatures = {
            ".pdf": lambda content: content.startswith(b"%PDF-"),
            ".png": lambda content: content.startswith(b"\x89PNG\r\n\x1a\n"),
            ".webp": lambda content: len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP",
        }
        for file_path in MATERIALS_FILES:
            if file_path.suffix != ".html":
                continue
            for link, has_download_attribute in self.html_links(file_path):
                if not has_download_attribute or not is_local_link(link):
                    continue
                target = link_target(file_path, link)
                suffix = target.suffix.lower()
                with self.subTest(file=target):
                    self.assertGreater(target.stat().st_size, 0)
                    if suffix == ".zip":
                        with zipfile.ZipFile(target) as archive:
                            self.assertIsNone(archive.testzip())
                    elif suffix in signatures:
                        with target.open("rb") as asset:
                            self.assertTrue(signatures[suffix](asset.read(12)))

    def test_website_and_resources_download_indexes_match(self):
        html_files = [file_path for file_path in MATERIALS_FILES if file_path.suffix == ".html"]
        indexes = []
        for file_path in html_files:
            indexes.append({
                unquote(urlsplit(link).path)
                for link, has_download_attribute in self.html_links(file_path)
                if has_download_attribute and is_local_link(link)
            })
        self.assertEqual(indexes[0], indexes[1])

    def test_learning_materials_page_contract(self):
        expected_categories = (
            "注音學習單（學齡前）",
            "數字學習單（學齡前）",
            "積木卡_初階（學齡前）",
            "中秋節任務（學齡前）",
        )
        for file_path in MATERIALS_FILES:
            if file_path.suffix != ".html":
                continue
            content = file_path.read_text(encoding="utf-8")
            with self.subTest(file=file_path):
                self.assertIn('<main id="learning-materials"', content)
                self.assertIn('aria-current="page"', content)
                self.assertIn('aria-label="主要導覽"', content)
                self.assertIn('>回到育伴首頁</a>', content)
                for category in expected_categories:
                    self.assertIn(f"<summary>{category}</summary>", content)

    def test_all_local_markdown_links_exist(self):
        markdown_link_pattern = re.compile(r"\]\(([^)]+)\)")
        for file_path in MATERIALS_FILES:
            if file_path.suffix != ".md":
                continue
            content = file_path.read_text(encoding="utf-8")
            for link in markdown_link_pattern.findall(content):
                if not is_local_link(link):
                    continue
                with self.subTest(file=file_path, link=link):
                    self.assertTrue(link_target(file_path, link).is_file())


if __name__ == "__main__":
    unittest.main()