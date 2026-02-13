import unittest

from textnode import TextNode, TextType
from text_node_to_html_node import text_node_to_html_node
from split_nodes_delimiter import split_nodes_delimiter as snd
from split_nodes_delimiter import text_to_textnodes as ttt

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    def test_tnthn(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        node = TextNode("FAKE_NEWS", TextType.IMAGE, "REAL_NEWS")
        hn = text_node_to_html_node(node)
        self.assertEqual(hn.tag, "img")
        self.assertEqual(hn.value, "")
        self.assertEqual(hn.props['src'], "REAL_NEWS")
        self.assertEqual(hn.props['alt'], "FAKE_NEWS")
        node = TextNode("B", TextType.BOLD)
        hn = text_node_to_html_node(node)
        self.assertEqual(hn.tag, "b")
        self.assertEqual(hn.value, "B")
        node = TextNode("l",TextType.LINK,"url")
        hn = text_node_to_html_node(node)
        self.assertEqual(hn.tag,"a")
        self.assertEqual(hn.value,"l")
        self.assertEqual(hn.props["href"],"url")
    def test_snd(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        nn = snd([node], "`", TextType.CODE)
        enn = [
          TextNode("This is text with a ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" word", TextType.TEXT),
        ]
        #print(nn)
        self.assertEqual(len(nn),3)
        for i in range(len(nn)):
            self.assertEqual(nn[i],enn[i])
        node = TextNode("**BOLD**___no_****text", TextType.TEXT)
        nn = snd([node,enn[1]],"CHILDREN",1)
        enn = [
          TextNode("BOLD",TextType.BOLD),
          TextNode("",TextType.ITALIC),
          TextNode("no",TextType.ITALIC),
          TextNode("",TextType.BOLD),
          TextNode("text",TextType.TEXT),
          TextNode("code block",TextType.CODE)
        ]
        self.assertEqual(len(nn),len(enn))
        for i in range(len(nn)):
            self.assertEqual(nn[i],enn[i])
    def test_split_images(self):
        node = TextNode(
          "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
          TextType.TEXT,
        )
        new_nodes = snd([node])
        #print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_ttt(self):
        t = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        n = ttt(t)
        self.assertListEqual(
        [
          TextNode("This is ", TextType.TEXT),
          TextNode("text", TextType.BOLD),
          TextNode(" with an ", TextType.TEXT),
          TextNode("italic", TextType.ITALIC),
          TextNode(" word and a ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" and an ", TextType.TEXT),
          TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
          TextNode(" and a ", TextType.TEXT),
          TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        n)


if __name__ == "__main__":
    unittest.main()
