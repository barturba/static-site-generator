import unittest

from htmlnode import HTMLNode
from main import extract_title, generate_page


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is the title"
        self.assertEqual("This is the title", extract_title(markdown))

    def test_extract_title_missing_title(self):
        markdown = "This is the title"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    # TODO: extract title: strip whitespace
    # TODO: extract title: multiline
    # TODO: replace title
    # TODO: replace content

    # def test_extract_title_missing_title(self):
    #     markdown = "This is the title"
    #     with self.assertRaises(ValueError):
    #         extract_title(markdown)

    def test_generate_page(self):
        from_path = "content/index.md"
        template_path = "template.html"
        dest_path = "public"
        self.assertEqual(None, generate_page(from_path, template_path, dest_path))


if __name__ == "__main__":
    unittest.main()
