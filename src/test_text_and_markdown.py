import unittest
from text_and_markdown import *
from html_nodes import *

class TestBlockToBlockType(unittest.TestCase):
    def test_ideal_case(self):
        example = """### This is the heading of an example document

## Section 1

This is an example of a markdown document, for the purpose of testing.

## Section 2

Following is an example of a code block.

```Some code
blablabla
etc```

Following is an example of an unordered list.

- list item 1
- list item 2
- list item 3

Following is an example of an ordered list.

1. list item 1
2. list item 2
3. list item 3

## A quote from poetry

> Leaves are falling
> western winds are blowing
> always remember."""
        blocks = markdown_to_blocks(example)
        blocktypes = list(map(block_to_blocktype, blocks))
        self.assertListEqual(blocktypes, [BlockType.HEADING,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH,
                                      BlockType.CODE,
                                      BlockType.PARAGRAPH,
                                      BlockType.UNORDERED_LIST,
                                      BlockType.PARAGRAPH,
                                      BlockType.ORDERED_LIST,
                                      BlockType.HEADING,
                                      BlockType.QUOTE])
    def test_incorrect_case(self):
        example = """### This is the heading of an example document

## Section 1

This is an example of a markdown document, for the purpose of testing.

## Section 2

Following is an example of a code block.

```Some code
blablabla
etc```and some more text

Following is an example of an unordered list.

- list item 1
-list item 2
- list item 3

Following is an example of an ordered list.

1. list item 1
2 list item 2
3. list item 3

## A quote from poetry

Leaves are falling
> western winds are blowing
> always remember."""
        blocks = markdown_to_blocks(example)
        blocktypes = list(map(block_to_blocktype, blocks))
        self.assertListEqual(blocktypes, [BlockType.HEADING,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH])
        
class TestExtractMarkdownImages(unittest.TestCase):
    def test_images(self):
        teststring = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(teststring)
        self.assertEqual(result, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
    def test_images_with_urls(self):
        teststring = "[A link in the beginning](http://wp.pl). This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), also: a [link](http://boot.dev)."
        result = extract_markdown_images(teststring)
        self.assertEqual(result, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
    def test_links_with_images(self):
        teststring = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), also: a [link](http://boot.dev)."
        result = extract_markdown_links(teststring)
        self.assertEqual(result, [('link', 'http://boot.dev')])
    def test_links_with_images_harder(self):
        teststring = "[A link in the beginning](http://wp.pl). This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), also: a [link](http://boot.dev)."
        result = extract_markdown_links(teststring)
        self.assertEqual(result, [('A link in the beginning', 'http://wp.pl'),('link', 'http://boot.dev')])

class TestMarkDownToBlocks(unittest.TestCase):
    def test_general(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_empty_paragraphs(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items





"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestSplitNodesDelimiter(unittest.TestCase):
    def testSplitBold(self):
        self.testnode = TextNode("This text contains some text, including **bold test** as well as _italic text_ and some python code: `lambda x: x+1`. Also some more **bold text** and _italics_. Why not some more `code`.", TextType.PLAIN)
        splitboldnodes = split_nodes_delimiter([self.testnode], "**", TextType.BOLD)
        self.assertEqual(len(splitboldnodes), 5)
        self.assertEqual(splitboldnodes[0].text_type, TextType.PLAIN)
        self.assertEqual(splitboldnodes[1].text_type, TextType.BOLD)
        self.assertEqual(splitboldnodes[1].text, "bold test")
        self.assertEqual(splitboldnodes[2].text, " as well as _italic text_ and some python code: `lambda x: x+1`. Also some more ")
        self.assertEqual(splitboldnodes[3].text_type, TextType.BOLD)
    def testMultipleSplits(self):
        self.testnode = TextNode("This text contains some text, including **bold test** as well as _italic text_ and some python code: `lambda x: x+1`. Also some more **bold text** and _italics_. Why not some more `code`.", TextType.PLAIN)
        splitboldnodes = split_nodes_delimiter([self.testnode], "**", TextType.BOLD)
        splititalicnodes = split_nodes_delimiter(splitboldnodes, "_", TextType.ITALIC)
        splitcodenodes = split_nodes_delimiter(splititalicnodes, "`", TextType.CODE)
        self.assertEqual(len(splitcodenodes), 13)
        self.assertEqual(splitcodenodes[0].text_type, TextType.PLAIN)
        self.assertEqual(splitcodenodes[0].text, "This text contains some text, including ")
        self.assertEqual(splitcodenodes[1].text_type, TextType.BOLD)
        self.assertEqual(splitcodenodes[1].text, "bold test")
        self.assertEqual(splitcodenodes[3].text_type, TextType.ITALIC)
        self.assertEqual(splitcodenodes[3].text, "italic text")
        self.assertEqual(splitcodenodes[5].text_type, TextType.CODE)
        self.assertEqual(splitcodenodes[5].text, "lambda x: x+1")
        self.assertEqual(splitcodenodes[9].text_type, TextType.ITALIC)
        self.assertEqual(splitcodenodes[9].text, "italics")
        self.assertEqual(splitcodenodes[11].text_type, TextType.CODE)
        self.assertEqual(splitcodenodes[11].text, "code")
        
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

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a link node", TextType.LINK, "https://github.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://github.com")
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
        node = TextNode("This is a link node", TextType.LINK, "https://github.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://github.com")
        self.assertNotEqual(node, node2)
        
        node = TextNode("This is a link node", TextType.LINK, "https://github.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

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
        
class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """# Title should be this

Some other stuff

> A quote
> continues"""
        title = extract_title(md)
        self.assertEqual(title, "Title should be this")
    
    def test_extract_title_from_middle(self):
        md = """### This is a level 3 heading

This is some paragraph

## This is level 2 heading

# Title should be this

Some more text

## Some other heading
"""
        title = extract_title(md)
        self.assertEqual(title, "Title should be this")



if __name__ == "__main__":
    unittest.main()
