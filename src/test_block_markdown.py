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
                            create_code_node,
                            markdown_to_html_node,
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
    # def test_ul_node(self):
    #     markdown_block = "- **Bold Item 1**\n- *Italic Item 2*\n- **Bold** and *Italic Item 3*"
    #     actual_output = create_ul_node(markdown_block)
    #     expected_output = ParentNode(
    #         "ul",
    #         [
    #             ParentNode("li", 
    #                        [
    #                            LeafNode("b", "Bold Item 1")
    #                         ]
    #                        ),
    #             ParentNode("li", 
    #                        [
    #                            LeafNode("i", "Italic Item 2")
    #                         ]
    #                        ),
    #             ParentNode("li",
    #                        [LeafNode("b", "Bold"),
    #                         LeafNode(None, " and "),
    #                        LeafNode("i", "Italic Item 3")
    #                        ]
    #                        )
    #         ]
    #         )
    #     self.maxDiff = None
    #     print(f"Actual Output: {actual_output}")
    #     print(f"Expected Output: {expected_output}")
    #     self.assertEqual(actual_output, expected_output) 

    # def test_code_node(self):
    #     markdown_block = """
    #                     ```
    #                     This is a code block.
    #                     for loop in loops:
    #                         do.stuff()
    #                     return fat_stuff
    #                     ```
    #                     """
    #     actual_output = create_code_node(markdown_block)
    #     expected_output = ParentNode(
    #                         "pre",
    #                         [
    #                             LeafNode("code", """This is a code block.
    #                     for loop in loops:
    #                         do.stuff()
    #                     return fat_stuff
    #                     """)
    #                         ]
    #                     )
        
    #     self.maxDiff = None
    #     print(f"Actual Output: {actual_output}")
    #     print(f"Expected_Output: {expected_output}")
    #     self.assertEqual(actual_output, expected_output)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )




if __name__ == "__main__":
    unittest.main()