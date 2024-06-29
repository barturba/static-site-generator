import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        expected_output = " href='https://www.google.com' target='_blank' " 

        output = node.props_to_html()
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()