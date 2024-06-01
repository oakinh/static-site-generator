import re
from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        new_blocks.append(block)
    return new_blocks


def block_to_block_type(markdown_block):
    if (
        markdown_block.startswith("# ")
        or markdown_block.startswith("## ")
        or markdown_block.startswith("### ")
        or markdown_block.startswith("#### ")
        or markdown_block.startswith("##### ")
        or markdown_block.startswith("###### ")
        ):
        return block_type_heading
    elif markdown_block.startswith("```"):
        if not markdown_block.endswith("```"):
            raise ValueError("Invalid markdown, code block must be properly closed")
        return block_type_code
    elif markdown_block.startswith(">"):
        splits = markdown_block.splitlines()
        for split in splits:
            if not split.startswith(">"):
                raise ValueError("Invalid markdown, each line in a quote block must start with a '>' character")
        return block_type_quote
    elif markdown_block.startswith("*") or markdown_block.startswith("-"):
        splits = markdown_block.splitlines()
        for split in splits:
            if not (split.startswith("*") or split.startswith("-")):
                raise ValueError("Invalid markdown, each line in an unordered list block must start with a '*' or '-' character")
        return block_type_unordered_list
    elif markdown_block.startswith("1."):
        splits = markdown_block.splitlines()
        base_pattern = "{}."
        line_number = 0
        for split in splits:
            line_number += 1
            pattern = base_pattern.format(line_number)
            if not bool(re.match(pattern, split)):
                raise ValueError("Invalid markdown, each line in an ordered list must start first with '1.' and increment by 1 thereafter")
        return block_type_ordered_list
    return block_type_paragraph

def create_paragraph_node(markdown_block):
    lines = markdown_block.split("\n")
    paragraph = " ".join(lines)
    textnodes = text_to_textnodes(paragraph)
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    return ParentNode(tag="p", children=children)


def create_blockquote_node(markdown_block):
    lines = markdown_block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    textnodes = text_to_textnodes(text)
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    return ParentNode(tag="blockquote", children=children)

def create_ul_node(markdown_block):
    lines = markdown_block.split("\n")
    stripped_lines = []
    for line in lines:
        stripped_line = re.sub(r'^\s*[-+*]\s+', '', line)
        stripped_lines.append(stripped_line)
    html_nodes = []
    for line in stripped_lines:
        text_nodes = text_to_textnodes(line)
        children = []
        for node in text_nodes:
            children.append(text_node_to_html_node(node))
        html_nodes.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=html_nodes)

def create_ol_node(markdown_block):
    lines = markdown_block.split("\n")
    stripped_lines = []
    for line in lines:
        stripped_line = re.sub(r'^\s*[0-9]\.\s+', '', line)
        stripped_lines.append(stripped_line)
    html_nodes = []
    for line in stripped_lines:
        text_nodes = text_to_textnodes(line)
        children = []
        for node in text_nodes:
            children.append(text_node_to_html_node(node))
        html_nodes.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=html_nodes)


def create_code_node(markdown_block):
    processed_lines = []
    processing = False
    for line in markdown_block.split('\n'):
        if not processing:
            if "```" in line:
                processing = True
                if processing:
                    new_line = line.split("```")
                    processed_lines.append(new_line[1])
        elif processing:
            if "```" in line:
                processing = False
            else:
                processed_lines.append(line)
    code_block = '\n'.join(processed_lines)
    child = LeafNode(tag="code", value=code_block)
    return ParentNode(tag="pre", children=[child])


def create_heading_node(markdown_block):
    header_count = 0
    trimmed_block = markdown_block.lstrip("# ")
    textnodes = text_to_textnodes(trimmed_block)
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    for c in markdown_block:
        if c == "#":
            header_count += 1
        else:
            break
    return ParentNode(tag=f"h{header_count}", children=children)
        

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        if block_to_block_type(block) == block_type_code:
            children.append(create_code_node(block))
        elif block_to_block_type(block) == block_type_heading:
            children.append(create_heading_node(block))
        elif block_to_block_type(block) == block_type_ordered_list:
            children.append(create_ol_node(block))
        elif block_to_block_type(block) == block_type_unordered_list:
            children.append(create_ul_node(block))
        elif block_to_block_type(block) == block_type_paragraph:
            children.append(create_paragraph_node(block))
        elif block_to_block_type(block) == block_type_quote:
            children.append(create_blockquote_node(block))
        else:
            raise ValueError("Invalid block type")
    return ParentNode(tag="div", children=children)