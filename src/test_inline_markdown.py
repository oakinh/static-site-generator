import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node
)

class TestExtractMarkDownImages(unittest.TestCase):
    def test_1(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected_output = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertEqual(extract_markdown_images(text), expected_output)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_links_extractions(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected_output = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(extract_markdown_links(text), expected_output)

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_nodes_1(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected_output = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_multiple(self):
        old_nodes = [TextNode("This is text with a **bolded** word", text_type_text),
                TextNode("This is a text with an *italic* word", text_type_text),
                TextNode("This is text with `coded words`", text_type_text)
                ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", text_type_code)
        expected_output = [
                TextNode("This is text with a **bolded** word", text_type_text),
                TextNode("This is a text with an *italic* word", text_type_text),
                TextNode("This is text with ", text_type_text),
                TextNode("coded words", text_type_code),
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_3(self):
        old_nodes = [TextNode("`coded words`", text_type_code),
                TextNode("This is a text with an *italic* word", text_type_text),
                TextNode("This is text with a **bolded** word", text_type_text),
                ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", text_type_code)
        expected_output = [TextNode("`coded words`", text_type_code),
                TextNode("This is a text with an *italic* word", text_type_text),
                TextNode("This is text with a **bolded** word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_fail_delimiter_count(self):
        text_nodes = [TextNode("Look at the **bold we created.", text_type_text),
                     TextNode("This is an *italic* text highlighting history.", text_type_text),
                    TextNode("This is a normal text", text_type_text)
        ]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(text_nodes, "**", text_type_bold)
        self.assertTrue("The delimiter provided hasn't been properly closed." in str(context.exception))

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )
# Every test below this line are from the course

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()