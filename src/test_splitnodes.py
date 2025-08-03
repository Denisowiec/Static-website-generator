import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_link,split_nodes_image

class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](http://wp.pl) and another [link](http://google.pl)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "http://wp.pl"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "link", TextType.LINK, "http://google.pl"
                ),
            ],
            new_nodes,
        )
    def test_split_images_mixed_with_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), a [link](http://wp.pl) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(", a [link](http://wp.pl) and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links_mixed_with_images(self):
        node = TextNode(
            "This is text with a [link](http://wp.pl), an ![image](https://i.imgur.com/zjjcJKZ.png) and another [link](http://google.pl)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "http://wp.pl"),
                TextNode(", an ![image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.PLAIN),
                TextNode(
                    "link", TextType.LINK, "http://google.pl"
                ),
            ],
            new_nodes,
        )