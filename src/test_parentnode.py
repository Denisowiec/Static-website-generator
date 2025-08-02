import unittest
from parentnode import ParentNode
from leafnode import LeafNode

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