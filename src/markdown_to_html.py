from htmlnode import HTMLNode, LeafNode, ParentNode
from blocktype import BlockType, block_to_block_type
from markdown_to_blocks import markdown_to_blocks
from split_nodes_delimiter import text_to_textnodes
from text_node_to_html_node import text_node_to_html_node

def markdown_to_html_node(markdown):
    b_ = markdown_to_blocks(markdown)
    c_nodes = [block_to_html_node(b) for b in b_]
    return ParentNode("div",c_nodes)


def block_to_html_node(b):
    tpe = block_to_block_type(b)
    tag = None
    inner_tag = None
    slices = []
    match tpe:
        case BlockType.HEADING:
            count = 0
            for ch in b:
                if ch == "#":
                    count += 1
                else:
                    break
            tag = f"h{count}"
            slices = [b[(count+1):]]
        case BlockType.QUOTE:
            tag = "blockquote"
            f = lambda l:l[(1 if len(l)<2 or l[1] != ' ' else 2):]
            slices = ['\n'.join([f(l) for l in b.split('\n')])]
        case BlockType.CODE:
            tag = "pre"
            slices = ['`'+b[4:-2]]
        case BlockType.PARAGRAPH:
            tag = "p"
            slices = [b.replace('\n',' ')]
        case BlockType.UNORDERED_LIST:
            tag = "ul"
            inner_tag = "li"
            slices = [l[2:] for l in b.split('\n')]
        case BlockType.ORDERED_LIST:
            tag = "ol"
            inner_tag = "li"
            slices = [l[(l.find('.')+2):] for l in b.split('\n')]
    
    p_node = ParentNode(tag,[])
    
    for s in slices:
        tns = text_to_textnodes(s)
        lns = [text_node_to_html_node(tn) for tn in tns]
        if inner_tag:
            p_node.children.append(ParentNode(inner_tag,lns))
        else:
            p_node.children.extend(lns)
    
    return p_node
    
def extract_title(md):
    start = md.find("# ")
    while start > 0 and md[start-1] != "\n":
        start = md.find("# ",start+1)
    if start == -1:
        raise Exception("Could not locate header of type h1.")
    end = md.find("\n",start+1)
    if end == -1:
        return md[(start+1):].strip()
    return md[(start+1):end].strip()
