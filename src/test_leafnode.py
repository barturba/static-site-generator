import unittest

from leafnode import LeafNode 

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node_1 = LeafNode(
            "p", 
            "This is a paragraph of text.", 
            None, 
            None,
            )
        self.assertEqual(
            node_1.to_html(), 
            '<p>This is a paragraph of text.</p>'
            )

        node_2 = LeafNode(
            "a", 
            "Click me!", 
            None,
            {"href": "https://www.google.com"}
            )
        self.assertEqual(
            node_2.to_html(), 
            '<a href="https://www.google.com">Click me!</a>'
            )

        # node_2 = HTMLNode(
        #     "div",
        #     "Hello, world!",
        #     None,
        #     {"class": "greeting", "href": "https://boot.dev"},
        # )
        # self.assertEqual(
        #     node_2.props_to_html(),
        #     ' class="greeting" href="https://boot.dev"',
        # )

if __name__ == "__main__":
    unittest.main()