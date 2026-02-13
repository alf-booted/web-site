import os
import sys
from textnode import TextNode, TextType
from move_from_static_to_public import move_from_static_to_public
from generate_page import generate_pages_recursive

def main():
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
    move_from_static_to_public("../docs")
    generate_pages_recursive(
      "../content/",#os.path.join(basepath,"/content/"),
      "../template.html",#os.path.join(basepath,"/template.html"),
      "../docs/",#os.path.join(basepath,"/public/")
      basepath
    )

if __name__ == "__main__":
    main()
