import unittest
from leafnode import LeafNode

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