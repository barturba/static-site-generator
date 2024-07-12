import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_simple_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
                LeafNode(None, "normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>bold text</b>normal text<i>italic text</i>normal text</p>",
        )

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                None,
                [
                    LeafNode("b", "bold text"),
                    LeafNode(None, "normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "normal text"),
                ],
            )

    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", [])
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)

    def test_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
                LeafNode(None, "normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "normal text"),
            ],
            {"class": "paragraph"},
        )
        self.assertEqual(
            node.to_html(),
            '<p class="paragraph"><b>bold text</b>normal text<i>italic text</i>normal text</p>',
        )

    def test_nested_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "bold text"),
                        LeafNode(None, "normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "normal text"),
                    ],
                    {"class": "paragraph"},
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<div><p class="paragraph"><b>bold text</b>normal text<i>italic text</i>normal text</p></div>',
        )

    def test_multiple_levels_of_nesting(self):
        node = ParentNode(
            "body",
            [
                ParentNode(
                    "div",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "bold text"),
                                LeafNode(None, "normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "normal text"),
                            ],
                            {"class": "paragraph"},
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<body><div><p class="paragraph"><b>bold text</b>normal text<i>italic text</i>normal text</p></div></body>',
        )


if __name__ == "__main__":
    unittest.main()
