import unittest

from textnode import TextNode


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

if __name__ == "__main__":
    unittest.main()
