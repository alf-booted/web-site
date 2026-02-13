from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes,delimiter=None,text_type=None):
    d = {"*":TextType.BOLD,"_":TextType.ITALIC,"`":TextType.CODE}
    new_nodes = []
    for o_n in old_nodes:
        if o_n.text_type != TextType.TEXT:
            new_nodes.append(o_n)
            continue
        h = 0
        ct = TextType.TEXT
        for i in range(len(o_n.text)):
            oni = o_n.text[i]
            if (h <= i) and (oni == "`" or oni == "_" or oni == "*"):
                if ct == TextType.TEXT:
                    if oni == "*" and o_n.text[i+1] != "*":
                        continue
                    if h != i:
                        new_nodes.append(TextNode(o_n.text[h:i],ct))
                        h = i
                    ct = d[oni]
                    h = i+(2 if oni == "*" else 1)
                elif ct == d[oni]:
                    new_nodes.append(TextNode(o_n.text[h:i],ct))
                    ct = TextType.TEXT
                    h = i+(2 if oni == "*" else 1)
        if ct != TextType.TEXT:
            raise Exception(f"Type {ct} was not closed")
        if h < len(o_n.text):
            new_nodes.append(TextNode(o_n.text[h:],ct))
    old_nodes = new_nodes
    new_nodes = []
    for o_n in old_nodes:
        if o_n.text_type != TextType.TEXT:
            new_nodes.append(o_n)
            continue
        h = 0
        lon = len(o_n.text)
        for i in range(lon):
            if o_n.text[i] == "[" and i >= h:
                j = o_n.text.find("]",i+1)
                k = o_n.text.find("[",i+1)
                if k != -1 and k < j:
                    continue
                if i < j < lon-1 and o_n.text[j+1] == "(":
                    k = o_n.text.find(")",j+1)
                    if j < k < lon:
                        is_image = (i != 0 and o_n.text[i-1] == "!")
                        if h != i:
                            new_nodes.append(TextNode(
                              o_n.text[h:i-(1 if is_image else 0)],
                              TextType.TEXT
                            ))
                        new_nodes.append(TextNode(
                          o_n.text[i+1:j],
                          TextType.IMAGE if is_image else TextType.LINK,
                          o_n.text[j+2:k]
                        ))
                        h = k+1
        if h < lon:
            new_nodes.append(TextNode(o_n.text[h:],TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    return split_nodes_delimiter([TextNode(text,TextType.TEXT)])
