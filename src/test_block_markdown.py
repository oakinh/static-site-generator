import unittest

from block_markdown import (markdown_to_blocks,
                            block_type_paragraph,
                            block_to_block_type,
                            block_type_code,
                            block_type_heading,
                            block_type_ordered_list,
                            block_type_quote,
                            block_type_unordered_list,
                            create_ul_node,
                            )
from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = ("# This is a heading \n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it. \n\n* This is a list item \n* This is another list item")
        expected_output = [
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item \n* This is another list item"
        ]
        self.maxDiff = None
        self.assertEqual(markdown_to_blocks(markdown), expected_output)

class TestMarkdownBlockToBlockType(unittest.TestCase):
    def test_block_type_heading(self):
        markdown_block = "### This is a heading level 3"
        self.assertEqual(block_to_block_type(markdown_block), block_type_heading)

    def test_block_type_code_broken(self):
        markdown_block = "```This is a broken code block``"
        with self.assertRaises(ValueError) as context:
            block_to_block_type(markdown_block)
        self.assertEqual("Invalid markdown, code block must be properly closed", str(context.exception))

    def test_block_type_code(self):
        markdown_block = "``` This is a complete code block```"
        self.assertEqual(block_to_block_type(markdown_block), block_type_code)

    def test_quote_block(self):
        markdown_block = """>This is a quote\n>Here's another line\n>Here's a final line of the quote"""
        self.assertEqual(block_to_block_type(markdown_block), block_type_quote)

    def test_unordered_list_1(self):
        markdown_block = """- This is an unordered list\n- Here's another line\n- And another"""
        self.assertEqual(block_to_block_type(markdown_block), block_type_unordered_list)

    def test_ordered_list_1(self):
        markdown_block = """1. This is an ordered list\n2. Here's another line\n3. And a final line"""
        self.assertEqual(block_to_block_type(markdown_block), block_type_ordered_list)
    
    def test_ordered_list_2(self):
        markdown_block = """1. This is an out of order ordered list\n3. Here's the out of order line \n2. Here's another out of order line"""
        with self.assertRaises(ValueError) as context:
            block_to_block_type(markdown_block)
        self.assertEqual("Invalid markdown, each line in an ordered list must start first with '1.' and increment by 1 thereafter", str(context.exception))

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_ul_node(self):
        markdown_block = "- **Bold Item 1**\n- *Italic Item 2*\n- **Bold** and *Italic Item 3*"
        actual_output = create_ul_node(markdown_block)
        expected_output = ParentNode(
            "ul",
            [
                ParentNode("li", 
                           LeafNode("b", "Bold Item 1")
                           ),
                ParentNode("li", 
                           LeafNode("i", "Italic Item 2")
                           ),
                ParentNode("li",
                           [LeafNode("b", "Bold"),
                            LeafNode(None, " and "),
                           LeafNode("i", "Italic Item 3")
                           ]
                           )
            ]
            )
        self.maxDiff = None
        self.assertEqual(actual_output, expected_output)
        


if __name__ == "__main__":
    unittest.main()