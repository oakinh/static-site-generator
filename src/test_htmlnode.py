import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("<a>", "Hi my name is bob", None, {"href": "https://www.google.com"})
        expected_output = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected_output)
    

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected_output = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_output = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node.to_html(), expected_output)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_output = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_2(self):
        node = ParentNode(
            "d",
            [
                ParentNode(
                    "p",
                [
                    LeafNode("i", "italic text"),
                    LeafNode("b", "bold text"),
                    LeafNode(None, "Look at this loooooooong string of text")

                ],
                )
            ]
        )
        expected_output = "<d><p><i>italic text</i><b>bold text</b>Look at this loooooooong string of text</p></d>"
        self.assertEqual(node.to_html(), expected_output)


if __name__ == "__main__":
    unittest.main()