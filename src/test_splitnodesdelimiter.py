import unittest
from splitnodesdelimiter import split_nodes_delimiter
from textnode import TextNode, TextType

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
        