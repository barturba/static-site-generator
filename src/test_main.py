import unittest

from htmlnode import HTMLNode
from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is the title"
        self.assertEqual("This is the title", extract_title(markdown))

    def test_extract_title_missing_title(self):
        markdown = "This is the title"
        with self.assertRaises(ValueError):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
