import unittest

from leafnode import LeafNode
from textnode import TextNode, extract_markdown_links, split_nodes_delimiter
from textnode import extract_markdown_images
from textnode import text_node_to_html_node

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


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

    def test_split_nodes_code_block(self):
        node = TextNode(
            "This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ]
        )

    def test_split_nodes_bold(self):
        node = TextNode(
            "This is text with a **bold** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
            ]
        )

    def test_split_nodes_italic(self):
        node = TextNode(
            "This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ]
        )

    def test_split_nodes_missing_delimiter(self):
        node = TextNode(
            "This is text with an *italic word", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", text_type_italic)

    def test_split_nodes_no_delimiter(self):
        node = TextNode(
            "This is text with an italic word", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", text_type_italic)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        matches = extract_markdown_images(text)
        self.assertEqual
        (
            matches,
            [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
             ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        matches = extract_markdown_links(text)
        self.assertEqual
        (
            matches,
            [("link", "https://www.example.com"),
             ("another", "https://www.example.com/another")]
        )


if __name__ == "__main__":
    unittest.main()
