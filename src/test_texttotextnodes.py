import unittest
from texttotextnodes import text_to_textnodes
from textnode import TextNode, TextType

class TestTextToTextNode(unittest.TestCase):
    def test_general(self):
        example = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        processed = text_to_textnodes(example)
        self.assertListEqual(processed,
                             [TextNode("This is ", TextType.PLAIN),
                              TextNode("text", TextType.BOLD),
                              TextNode(" with an ", TextType.PLAIN),
                              TextNode("italic", TextType.ITALIC),
                              TextNode(" word and a ", TextType.PLAIN),
                              TextNode("code block", TextType.CODE),
                              TextNode(" and an ", TextType.PLAIN),
                              TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                              TextNode(" and a ", TextType.PLAIN),
                              TextNode("link", TextType.LINK, "https://boot.dev")])
    def test_link_in_beginning(self):
        example = "[This is a link](http://boot.dev) in the beginning of a sentence that also contains an ![image](image.jpg) and some **bold text**."
        processed = text_to_textnodes(example)
        self.assertListEqual(processed,
                             [TextNode("This is a link", TextType.LINK, "http://boot.dev"),
                              TextNode(" in the beginning of a sentence that also contains an ", TextType.PLAIN),
                              TextNode("image", TextType.IMAGE, "image.jpg"),
                              TextNode(" and some ", TextType.PLAIN),
                              TextNode("bold text", TextType.BOLD),
                              TextNode(".", TextType.PLAIN)])
    def test_image_in_beginning(self):
        example = "![This is an image](image.jpg) in the beginning of a sentence that also contains a [link](http://boot.dev) and some **bold text**."
        processed = text_to_textnodes(example)
        self.assertListEqual(processed,
                             [TextNode("This is an image", TextType.IMAGE, "image.jpg"),
                              TextNode(" in the beginning of a sentence that also contains a ", TextType.PLAIN),
                              TextNode("link", TextType.LINK, "http://boot.dev"),
                              TextNode(" and some ", TextType.PLAIN),
                              TextNode("bold text", TextType.BOLD),
                              TextNode(".", TextType.PLAIN)])

