import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("Header text before the image. ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) Footer text after the image.", text_type_text)
        new_nodes = split_nodes_image([node])
        expected_output = [
            TextNode("Header text before the image. ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" Footer text after the image.", text_type_text)
        ]
        self.maxDiff = None
        self.assertEqual(new_nodes, expected_output)

    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected_output = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ]
        self.maxDiff = None
        self.assertEqual(new_nodes, expected_output)

    def test_leading_image(self):
        node = TextNode(
            "![image](https://boot.dev) and a second ![second image](https://google.com)",
            text_type_text,
        )
        expected_output = [
            TextNode("image", text_type_image, "https://boot.dev"),
            TextNode(" and a second ", text_type_text),
            TextNode("second image", text_type_image, "https://google.com")
        ]
        self.maxDiff = None
        self.assertEqual(expected_output, split_nodes_image([node]))

    def test_large_quantity_images(self):
        node = TextNode("![image](https://gmail.com) and another image ![second image](https://youtube.com) this is a panda ![third image](https://pandas.com) oooh look a walrus ![fourth image](https://walruses.com)", text_type_text)
        expected_output = [
            TextNode("image", text_type_image, "https://gmail.com"),
            TextNode(" and another image ", text_type_text),
            TextNode("second image", text_type_image, "https://youtube.com"),
            TextNode(" this is a panda ", text_type_text),
            TextNode("third image", text_type_image, "https://pandas.com"),
            TextNode(" oooh look a walrus ", text_type_text),
            TextNode("fourth image", text_type_image, "https://walruses.com"),
        ]
        self.maxDiff = None
        self.assertEqual(expected_output, split_nodes_image([node]))

    def test_no_image(self):
        node = TextNode("This is a textnode with no images inside.", text_type_text)
        expected_output = [TextNode("This is a textnode with no images inside.", text_type_text)]
        self.assertEqual(expected_output, split_nodes_image([node]))

    def test_single_link(self):
        node = TextNode("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)", text_type_text)
        expected_output = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode("another", text_type_link, "https://www.example.com/another")
        ]
        self.maxDiff = None
        self.assertEqual(expected_output, split_nodes_link([node]))

    # Tests below this line are from the course

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()