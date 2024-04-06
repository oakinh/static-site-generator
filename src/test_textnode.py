import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_2(self):
        node = TextNode("This is my first test", "italics", "https://www.google.com")
        node2 = TextNode("This is my first test", "italics", "https://www.google.com")
        self.assertEqual(node, node2)

    def test_3(self):
        node = TextNode("This is my first test", "bold", "https://www.google.com")
        node2 = TextNode("This is my first test", "italics", "https://www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_4(self):
        node = TextNode("This is not my first test", "bold", "https://www.google.com")
        node2 = TextNode("This is my first test", "italics", "https://www.google.com")
        self.assertNotEqual(node, node2)


class TestTextNodetoHTMLNode(unittest.TestCase):
    
    def test_bold_text_to_leaf_node(self):
        text_node = TextNode(text="hello", text_type="bold")
        leaf_node = text_node_to_html_node(text_node)
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "hello")

    def test_image_to_leaf_node(self):
        text_node = TextNode(text="This is an image of a panda", text_type="image", url="www.pandas.com")
        leaf_node = text_node_to_html_node(text_node)
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertEqual(leaf_node.props, {"src": "www.pandas.com", "alt": "This is an image of a panda"})

    def test_invalid_text_type(self):
        text_node = TextNode(text="destruct", text_type="farm")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertTrue("TextNode not a valid text-type" in str(context.exception))

    def test_link_type_to_leaf_node(self):
        text_node = TextNode(text="Click this link", text_type="link", url="www.clickablelink.com")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.props, {"href": "www.clickablelink.com"})
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "Click this link")



if __name__ == "__main__":
    unittest.main()
