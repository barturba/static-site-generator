import unittest

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


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
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
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items" "",
            ],
        )

    def test_markdown_to_blocks_multiple_newlines(self):
        result = markdown_to_blocks(
            """This is **bolded** paragraph


This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items


"""
        )
        self.assertEqual(
            result,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_multiple_newlines_blank_spaces(self):
        result = markdown_to_blocks(
            """ This is **bolded** paragraph


     This is another paragraph with *italic* text and `code` here
 This is the same paragraph on a new line

     * This is a list
 * with items


"""
        )
        self.assertEqual(
            result,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\n This is the same paragraph on a new line",
                "* This is a list\n * with items",
            ],
        )

        pass

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)


if __name__ == "__main__":
    unittest.main()
