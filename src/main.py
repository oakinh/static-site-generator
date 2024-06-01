from textnode import TextNode
from copy_directory import copy_directory_contents
import os

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(base_dir, "../static")
    dest_dir = os.path.join(base_dir, "../public")
    
    copy_directory_contents(source_dir, dest_dir)

main()