import unittest
from markdown_to_blocks import markdown_to_blocks as mtb
from blocktype import BlockType, block_to_block_type as btbt
from markdown_to_html import markdown_to_html_node, extract_title

class TestMarkdown(unittest.TestCase):
    def test_mtb(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = mtb(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_btbt(self):
        b = "### Hey###"
        self.assertEqual(btbt(b),BlockType.HEADING)
        b = "```\nprint('Hello,')\nprint('World!')```"
        self.assertEqual(btbt(b),BlockType.CODE)
        b = "> be me\n>be hungry\n> eat dinner\n>still hungry"
        self.assertEqual(btbt(b),BlockType.QUOTE)
        b = "- Hello,\n- there..."
        self.assertEqual(btbt(b),BlockType.UNORDERED_LIST)
        b = "1. Hello,\n2. There\n3. \n4. still reading?"
        self.assertEqual(btbt(b),BlockType.ORDERED_LIST)
        b = "1. Hello,\n3. There\n3. \n4. still?"
        self.assertEqual(btbt(b),BlockType.PARAGRAPH)
        b = "-Hello,\n- there.."
        self.assertEqual(btbt(b),BlockType.PARAGRAPH)

    def test_markdown_to_html_node(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
          html,
          "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
          html,
          "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

        md = """
### H3
            
## H2

>Hello
> World

1. ORDER

-  NoOrder
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
          html,
          "<div><h3>H3</h3><h2>H2</h2><blockquote>Hello\nWorld</blockquote><ol><li>ORDER</li></ol><ul><li> NoOrder</li></ul></div>"
        )
    def test_xtitle(self):
        md = "# Hello guy   \nfawkes"
        title = extract_title(md)
        self.assertEqual(title,"Hello guy")
        md = "## Bye #hi \n# hello#"
        title = extract_title(md)
        self.assertEqual(title,"hello#")


if __name__ == "__main__":
    unittest.main()
