import unittest

from htmlnode import HTMLNode
from textnode import (
    TextNode,
    block_to_block_type,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from markdown_blocks import block_to_block_type, markdown_to_blocks

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TestMarkdown(unittest.TestCase):
    def test_markdown(self):
        result = markdown_to_blocks(
            """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        )
        self.assertEqual(
            result,
            [
                HTMLNode(
                    "div",
                    None,
                    [
                        HTMLNode(
                            "p",
                            None,
                            [
                                TextNode("This is ", text_type_text),
                                TextNode("bolded", text_type_bold),
                                TextNode("paragraph", text_type_text),
                            ],
                        ),
                        HTMLNode(
                            "p",
                            None,
                            [
                                TextNode(
                                    "This is another paragraph with ", text_type_text
                                ),
                                TextNode("italic", text_type_italic),
                                TextNode("text and ", text_type_text),
                                TextNode("code", text_type_code),
                                TextNode("here", text_type_text),
                                TextNode(
                                    "This is the same paragraph on a new line",
                                    text_type_text,
                                ),
                            ],
                        ),
                        HTMLNode(
                            "ul",
                            None,
                            [
                                HTMLNode(
                                    "li",
                                    None,
                                    TextNode("THis is a list", text_type_text),
                                ),
                                HTMLNode(
                                    "li",
                                    None,
                                    TextNode("with items", text_type_text),
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
