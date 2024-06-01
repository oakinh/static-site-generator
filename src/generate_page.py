from pathlib import Path
from block_markdown import markdown_to_html_node
from htmlnode import ParentNode
import os

def extract_title(markdown):
    markdown_rows = markdown.split("\n")
    for row in markdown_rows:
        if row[0] == "#":
            return row
    raise Exception("No h1 header found. All pages need a single h1 header")

def generate_page(source_path, template_path, destination_path):
    if not os.path.exists(source_path):
        raise ValueError(f"Invalid source directory path: {source_path}. Please make sure the path exists.")
    if not os.path.exists(template_path):
        raise ValueError(f"Invalid template path: {template_path}. Please make sure the path exists.")
    

    print(f"Generating page from {source_path} to {destination_path} using {template_path}")
    source_markdown = Path(source_path).read_text()
    template_file = Path(template_path).read_text()
    ParentNode = markdown_to_html_node(source_markdown)
    print(f"ParentNode: {ParentNode}")
    HTML = ParentNode.to_html()
    title = extract_title(source_markdown)
    HTML_file = template_file.replace("{{ Title }}", title)
    HTML_file = HTML_file.replace("{{ Content }}", HTML)
    Path(destination_path).write_text(HTML_file)

