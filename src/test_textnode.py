import unittest

from leafnode import LeafNode
from textnode import TextNode, block_to_block_type, extract_markdown_links, markdown_to_blocks, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import extract_markdown_images
from textnode import text_node_to_html_node

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


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

    def test_split_nodes_bold_multiple(self):

        node = TextNode(
            "This is text with a **bold** word and **another**. More text after.", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
                TextNode(". More text after.", text_type_text),
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

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )

        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image,
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode("second image", text_type_image,
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
            ]

        )

    def test_split_nodes_image_after(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and text after.",
            text_type_text,
        )

        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image,
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode("second image", text_type_image,
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
                TextNode(" and text after.", text_type_text),
            ]

        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )

        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link,
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode("second link", text_type_link,
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
            ]

        )

    def test_split_nodes_text_after(self):
        node = TextNode(
            "This is text with a [text](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second text](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and text after.",
            text_type_text,
        )

        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("text", text_type_link,
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode("second text", text_type_link,
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
                TextNode(" and text after.", text_type_text),
            ]

        )

    def test_split_nodes(self):

        new_nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)")
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is ", text_type_text),
                             TextNode("text", text_type_bold),
                             TextNode(" with an ", text_type_text),
                             TextNode("italic", text_type_italic),
                             TextNode(" word and a ", text_type_text),
                             TextNode("code block", text_type_code),
                             TextNode(" and an ", text_type_text),
                             TextNode(
                                 "image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                             TextNode(" and a ", text_type_text),
                             TextNode("link", text_type_link,
                                      "https://boot.dev"),
                         ])

    def test_split_nodes_multiple(self):

        new_nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev). And *even* **more** text and links [link](https://boot.dev) ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)")
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is ", text_type_text),
                             TextNode("text", text_type_bold),
                             TextNode(" with an ", text_type_text),
                             TextNode("italic", text_type_italic),
                             TextNode(" word and a ", text_type_text),
                             TextNode("code block", text_type_code),
                             TextNode(" and an ", text_type_text),
                             TextNode(
                                 "image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                             TextNode(" and a ", text_type_text),
                             TextNode("link", text_type_link,
                                      "https://boot.dev"),
                             TextNode(". And ", text_type_text),
                             TextNode("even", text_type_italic),
                             TextNode(" ", text_type_text),
                             TextNode("more", text_type_bold),
                             TextNode(" text and links ", text_type_text),
                             TextNode("link", text_type_link,
                                      "https://boot.dev"),
                             TextNode(" ", text_type_text),
                             TextNode(
                                 "image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                         ])

    def test_markdown_to_blocks(self):
        result = markdown_to_blocks("""This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items""")
        self.assertEqual(result,
                         [
                             "This is **bolded** paragraph",
                             "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                             "* This is a list\n* with items""",
                         ])

    def test_markdown_to_blocks_multiple_newlines(self):
        result = markdown_to_blocks("""This is **bolded** paragraph


This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items


""")
        self.assertEqual(result,
                         [
                             "This is **bolded** paragraph",
                             "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                             "* This is a list\n* with items",
                         ])

    def test_markdown_to_blocks_multiple_newlines_blank_spaces(self):
        result = markdown_to_blocks(
            """ This is **bolded** paragraph


     This is another paragraph with *italic* text and `code` here
 This is the same paragraph on a new line

     * This is a list
 * with items


""")
        self.assertEqual(
            result,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\n This is the same paragraph on a new line",
                "* This is a list\n * with items",
            ])

        pass

    def test_block_to_block_type_heading(self):
        result = block_to_block_type("# This is a heading")
        self.assertEqual(result, block_type_heading)

    def test_block_to_block_type_code_block(self):
        result = block_to_block_type("```This is a code block.```")
        self.assertEqual(result, block_type_code)

    def test_block_to_block_type_quote(self):
        result = block_to_block_type(
            ">This is a quote block\n>This is the second line in a quote block.")
        self.assertEqual(result, block_type_quote)

    def test_block_to_block_type_not_quote(self):
        result = block_to_block_type(
            ">This is a quote block\nThis is the second line in a quote block.")
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()
