import os
from textnode import TextNode, TextType
from move_from_static_to_public import move_from_static_to_public
from generate_page import generate_pages_recursive

def main():
    move_from_static_to_public()
    generate_pages_recursive("../content/","../template.html","../public/")

if __name__ == "__main__":
    main()
