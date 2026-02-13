import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_pth(self):
        node1 = HTMLNode(props = {"a": "aa", "b": "bb"})
        self.assertEqual(node1.props_to_html(), ' a="aa" b="bb"')
        node2 = HTMLNode(props = {"href": "google.com"})
        self.assertEqual(node2.props_to_html(), ' href="google.com"')
        node3 = HTMLNode()
        self.assertEqual(node3.props_to_html(), '')
    def test_thm(self):
        node = LeafNode("a","power")
        self.assertEqual(node.to_html(), "<a>power</a>")
        node = LeafNode("p","Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("40")
        self.assertEqual(node.to_html(), "40")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
          parent_node.to_html(),
          "<div><span><b>grandchild</b></span></div>",
        )
        parent_node = ParentNode("epic", [child_node, grandchild_node], {"a":"a"})
        self.assertEqual(
          parent_node.to_html(),
          '<epic a="a"><span><b>grandchild</b></span><b>grandchild</b></epic>'
        )

if __name__ == "__main__":
    unittest.main()
