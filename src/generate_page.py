from pathlib import Path
from block_markdown import markdown_to_html_node
from htmlnode import ParentNode
import os
import shutil

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
    HTML = ParentNode.to_html()
    title = extract_title(source_markdown)
    HTML_file = template_file.replace("{{ Title }}", title)
    HTML_file = HTML_file.replace("{{ Content }}", HTML)

    dest_dir_path = os.path.dirname(destination_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    Path(destination_path).write_text(HTML_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path_content = os.path.abspath(dir_path_content)
    dest_dir_path = os.path.abspath(dest_dir_path)

    if not os.path.exists(dir_path_content):
        raise ValueError(f"Invalid source directory path: {dir_path_content}. Please make sure the path exists.")
    if not os.path.exists(template_path):
        raise ValueError(f"Invalid template path: {template_path}. Please make sure the path exists.")
    if not os.path.exists(dest_dir_path):
        try:
            os.mkdir(dest_dir_path)
        except Exception as e:
            print(f"Error: {str(e)} | Destination path did not exist, but also could not be created. Check to make sure there aren't errors in the destination_directory_path.")
    

    content_files = os.listdir(dir_path_content)

    for file in content_files:
        html_file = file.replace(".md", ".html")
        file_content_path = os.path.join(dir_path_content, file)
        file_destination_path = os.path.join(dest_dir_path, html_file)

        if os.path.isdir(file_content_path):
            print(f"{file} is a directory, recursing...")
            generate_pages_recursive(file_content_path, template_path, file_destination_path)
        elif os.path.isfile(file_content_path):
            print(f"Generating page from {file_content_path} to {file_destination_path}")
            generate_page(file_content_path, template_path, file_destination_path)
        else:
            raise ValueError(f"I have no idea what happened here. Source: {file_content_path} Dest: {file_destination_path}")