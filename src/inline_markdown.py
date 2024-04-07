import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
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