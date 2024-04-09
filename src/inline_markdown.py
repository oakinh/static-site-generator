import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            split_strings = node.text.split(delimiter)
            if node.text.count(delimiter) % 2 != 0:
                raise Exception("The delimiter provided hasn't been properly closed.")
            for index, string in enumerate(split_strings):
                if index % 2 == 0 and string:
                    new_nodes.append(TextNode(string, node.text_type))  
                elif index % 2 != 0:
                    new_nodes.append(TextNode(string, text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            images = extract_markdown_images(node.text)
            unprocessed = node.text
            for image in images:
                split_text = unprocessed.split(f"![{image[0]}]({image[1]})", 1)
                if split_text[0]:
                    new_node = [TextNode(split_text[0], text_type_text), TextNode(text=image[0], text_type=text_type_image, url=image[1])]
                    new_nodes.extend(new_node)
                elif not split_text[0]:
                    new_node = [TextNode(text=image[0], text_type=text_type_image, url=image[1])]
                    new_nodes.extend(new_node)
                unprocessed = split_text[1]
            if unprocessed:
                    new_nodes.append(TextNode(text=unprocessed, text_type=text_type_text))
        else:
            new_nodes.append(node)
    return new_nodes

# Images = [('image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'), ('second image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png')]
# Input/old_nodes.text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            links = extract_markdown_links(node.text)
            unprocessed = node.text
            for link in links:
                split_text = unprocessed.split(f"[{link[0]}]({link[1]})", 1)
                if len(split_text) != 2:
                    raise ValueError("Invalid markdown, link section not closed")
                if split_text[0]:
                    new_node = [TextNode(split_text[0], text_type_text), TextNode(text=link[0], text_type=text_type_link, url=link[1])]
                    new_nodes.extend(new_node)
                unprocessed = split_text[1]
            if unprocessed != "":
                    new_nodes.append(TextNode(text=unprocessed, text_type=text_type_text))
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text):
    textnode = [TextNode(text=text, text_type=text_type_text)]
    post_split_delimiter_bold = split_nodes_delimiter(textnode, "**", text_type_bold)
    post_split_delimiter_bold_italic = split_nodes_delimiter(post_split_delimiter_bold, "*", text_type_italic)
    post_split_delimiter_all = split_nodes_delimiter(post_split_delimiter_bold_italic, "`", text_type_code)
    post_delimiter_split_image = split_nodes_image(post_split_delimiter_all)
    post_delimiter_split_image_link = split_nodes_link(post_delimiter_split_image)
    return post_delimiter_split_image_link

