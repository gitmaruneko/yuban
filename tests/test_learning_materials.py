import re
import unittest
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
    def test_all_local_html_links_exist_and_are_downloadable(self):
        for file_path in MATERIALS_FILES:
            if file_path.suffix != ".html":
                continue
            parser = LinkParser()
            parser.feed(file_path.read_text(encoding="utf-8"))
            for link, has_download_attribute in parser.links:
                if not is_local_link(link):
                    continue
                with self.subTest(file=file_path, link=link):
                    self.assertTrue(has_download_attribute)
                    self.assertTrue(link_target(file_path, link).is_file())

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