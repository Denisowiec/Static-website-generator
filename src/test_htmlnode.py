import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()