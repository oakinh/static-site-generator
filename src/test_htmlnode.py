import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("<a>", "Hi my name is bob", None, {"href": "https://www.google.com"})
        expected_output = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_2(self):
        node = HTMLNode("<a>", "Hi my name is bob", None, None)
        expected_output = ""
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

    def test_to_html_3(self):
        node = ParentNode(
            "p",
            []
        )
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertTrue("Invalid: no children provided" in str(context.exception))

    def test_to_html_4(self):
        node = ParentNode(
            None,
            [
                LeafNode("i", "italic text"),
                LeafNode("b", "bold text"),
                LeafNode(None, "Look at this loooooooong string of text")
            ],
        )
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertTrue("Invalid: no tag provided" in str(context.exception))

    def test_to_html_5(self):
        node = ParentNode(
            "",
            [
                LeafNode("i", "italic text"),
                LeafNode("b", "bold text"),
                LeafNode(None, "Look at this loooooooong string of text")
            ],
        )
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertTrue("Invalid: no tag provided" in str(context.exception))



if __name__ == "__main__":
    unittest.main()