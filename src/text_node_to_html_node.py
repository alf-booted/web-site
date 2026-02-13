from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node:TextNode):
    t = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(t)
        case TextType.BOLD:
            return LeafNode(tag="b",value=t)
        case TextType.ITALIC:
            return LeafNode(tag="i",value=t)
        case TextType.CODE:
            return LeafNode(tag="code",value=t)
        case TextType.LINK:
            return LeafNode(tag="a",value=t,props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img",value="",props={"src":text_node.url,"alt":t})
        case _:
            raise Exception("Invalid text type provided.")
