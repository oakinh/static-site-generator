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
    print(new_nodes)
    return new_nodes

# Images = [('image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'), ('second image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png')]
# Input/old_nodes.text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"


#def split_nodes_link(old_nodes):




