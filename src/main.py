from textnode import TextNode
from copy_directory import copy_directory_contents
from generate_page import generate_pages_recursive, generate_page
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # source_dir = os.path.join(base_dir, "../static")
    # dest_dir = os.path.join(base_dir, "../public")
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_directory_contents(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()