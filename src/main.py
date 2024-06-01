from textnode import TextNode
from copy_directory import copy_directory_contents
from generate_page import generate_page
import os

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(base_dir, "../static")
    dest_dir = os.path.join(base_dir, "../public")
    
    copy_directory_contents(source_dir, dest_dir)

    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()