import unittest

from leafnode import LeafNode
from textnode import TextNode
from textnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold",
                        "https://www.google.com")
        node2 = TextNode("This is a text node", "bold",
                         "https://www.google.com")
        self.assertEqual(node, node2)

    def test_convert_invalid(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(
                TextNode("This is a bold text node", "bold_1", None)),

    def test_convert_bold(self):
        node_1 = TextNode("This is a bold text node", "bold", None)
        node_2 = LeafNode("b", "This is a bold text node", None)
        self.assertEqual(
            text_node_to_html_node(node_1),
            node_2
        )

    def test_convert_italic(self):
        node_1 = TextNode("This is an italic text node", "italic", None)
        node_2 = LeafNode("i", "This is an italic text node", None)
        self.assertEqual(
            text_node_to_html_node(node_1),
            node_2
        )

    def test_convert_code(self):
        node_1 = TextNode("This is a code text node", "code", None)
        node_2 = LeafNode("code", "This is a code text node", None)
        self.assertEqual(
            text_node_to_html_node(node_1),
            node_2
        )

    def test_convert_link(self):
        node_1 = TextNode("This is a link text node",
                          "link", "https://www.google.com")
        node_2 = LeafNode("a", "This is a link text node", None, {
                          "href": "https://www.google.com"})
        self.assertEqual(
            text_node_to_html_node(node_1),
            node_2
        )

    def test_convert_image(self):
        node_1 = TextNode(
            "This is an image text node",
            "image", "https://www.google.com"
        )
        node_2 = LeafNode("img", "", None, {
                          "src": "https://www.google.com", "alt": "This is an image text node"})
        self.assertEqual(
            text_node_to_html_node(node_1),
            node_2
        )


if __name__ == "__main__":
    unittest.main()
