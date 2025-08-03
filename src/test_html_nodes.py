import unittest
from text_and_markdown import *
from html_nodes import *

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node1 = HTMLNode("a", "This is a link", None, {"href": "http://boot.dev"})
        node2 = HTMLNode()
        node2.tag = "a"
        node2.value = "This is a link"
        node2.props = {"href": "http://boot.dev"}

        #self.assertEqual(node1.to_html(), node2.to_html)
        self.assertEqual(node1.props_to_html(), node2.props_to_html())
    def test_repr(self):
        node1 = HTMLNode("a", "This is a link", None, {"href": "http://boot.dev"})
        node2 = HTMLNode()
        node2.tag = "a"
        node2.value = "This is a link"
        node2.props = {"href": "http://boot.dev"}

        self.assertEqual(node1.__repr__(), node2.__repr__())

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "A link", {"href": "http://boot.dev"})
        self.assertEqual(node.to_html(), "<a href=\"http://boot.dev\">A link</a>")
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold Text", None)
        self.assertEqual(node.to_html(), "<b>Bold Text</b>")
    def test_leaf_to_html_img(self):
        node = LeafNode("img", None, {"src": "image.jpg", "alt": "This is an image"})
        self.assertEqual(node.to_html(), "<img src=\"image.jpg\" alt=\"This is an image\" />")

class TestParentNode(unittest.TestCase):
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
    
    def test_to_html_with_multiple_nested_grandchildren(self):
        grandchild1 = LeafNode("a", "This is a link", {"href": "http://boot.dev"})
        grandchild2 = LeafNode("b", "Bold Text")
        grandchild3 = LeafNode("span", "Some text")
        child1 = ParentNode("p", [grandchild1, grandchild2])
        child2 = ParentNode("p", [grandchild3])
        parent1 = ParentNode("body", [child1, child2])
        self.assertEqual(parent1.to_html(),
                         "<body><p><a href=\"http://boot.dev\">This is a link</a><b>Bold Text</b></p><p><span>Some text</span></p></body>"
                         )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
    def test_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<img src=\"image.jpg\" alt=\"This is an image\" />")

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
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

    def test_codeblock(self):
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
            """<div><pre><code>This is text that _should_ remain
the **same** even with inline stuff</code></pre></div>""",
        )
    def test_ordered_list(self):
        md = "### This is an ordered list\n\n1. First list item\n2. Second list item\n3. Third list item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><h3>This is an ordered list</h3><ol><li>First list item</li><li>Second list item</li><li>Third list item</li></ol></div>")

    def test_unordered_list(self):
        md = "### This is an unordered list\n\n- First list item\n- Second list item\n- Third list item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><h3>This is an unordered list</h3><ul><li>First list item</li><li>Second list item</li><li>Third list item</li></ul></div>")

    def test_link_in_beginning(self):
        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**."""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Tolkien Fan Club</h1><p><img src=\"images/tolkien.png\" alt=\"JRR Tolkien sitting\" /></p><p>Here's the deal, <b>I like Tolkien</b>.</p></div>")

if __name__ == "__main__":
    unittest.main()
