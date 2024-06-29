import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node_1 = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node_1.props_to_html(), ' href="https://www.google.com" target="_blank"')

        node_2 = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node_2.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

if __name__ == "__main__":
    unittest.main()