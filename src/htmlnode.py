

class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Cannot be called from base class")

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ''
        return ''.join([f' {k}="{self.props[k]}"' for k in self.props])

    def __repr__(self):
        ret = "HTMLNode;\n"
        ret += "no tag\n" if self.tag == None else f"Tag: {self.tag}\n"
        ret += "no value\n" if self.value == None else f"Value: {self.value}\n"
        ret += "0 children\n" if self.children == None or len(children) == 0 else f"{len(self.children)} children\n"
        ret += "Props: {self.props}\n"
        return ret



class LeafNode(HTMLNode):
    def __init__(self,tag,value=None,props=None):
        if value == None:
            value = tag
            tag = None
        super().__init__(tag,value,props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        ret = "HTMLNode;\n"
        ret += "no tag\n" if self.tag == None else f"Tag: {self.tag}\n"
        ret += "no value\n" if self.value == None else f"Value: {self.value}\n"
        ret += "Props: {self.props}\n"
        return ret

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,children=children,props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            raise ValueError("ParentNode must have list of children")
        return f'<{self.tag}{self.props_to_html()}>{"".join([c.to_html() for c in self.children])}</{self.tag}>'
