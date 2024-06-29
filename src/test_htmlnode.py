import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node_1 = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        node_2 = HTMLNode(None, None, None, {"href": "https://www.boot.dev", "target": "_blank"}) 
        expected_output_1 = " href='https://www.google.com' target='_blank' " 
        expected_output_2 = " href='https://www.boot.dev' target='_blank' " 

        output_1 = node_1.props_to_html()
        output_2 = node_2.props_to_html()

        self.assertEqual(output_1, expected_output_1)
        self.assertEqual(output_2, expected_output_2)

if __name__ == "__main__":
    unittest.main()