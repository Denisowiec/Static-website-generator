import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "undordered list"
    ORDERED_LIST = "ordered_list"

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
        return f"\nTextNode({self.text}, {self.text_type.value}, {self.url})"
    

def block_to_blocktype(single_block):
    # Check if it is heading
    test = re.findall(r"^#{1,6} ", single_block)
    if len(test) > 0:
        return BlockType.HEADING
    
    # Check if it is quote
    brackets = re.findall(r"^> |^>\n", single_block, re.M)
    newlines = single_block.split("\n")
    if len(brackets) == len(newlines):
        return BlockType.QUOTE
    
    # Check if it is block code
    test = re.findall(r"^```|```$", single_block)
    if len(test) == 2:
        return BlockType.CODE
    
    # Check if it is an unordered list
    listitems = re.findall(r"^- ", single_block, re.M)
    newlines = single_block.split("\n")
    if len(listitems) == len(newlines):
        return BlockType.UNORDERED_LIST
    
    # Check if it is an ordered list
    listitems = re.findall(r"(^|\n)\d+. ", single_block)
    newlines = single_block.split("\n")
    if len(listitems) == len(newlines):
        return BlockType.ORDERED_LIST
    
    # If it's none of the above, it's a paragraph
    return BlockType.PARAGRAPH

def extract_markdown_images(text):
    splits = re.findall(r"!\[.*?\]\(.*?\)", text)
    result_list = []
    for s in splits:
        # This weird expression below extracts just the alt text, without the surrounding brackets.
        alt_text = re.findall(r"\[.*?\]", s)[0][1:-1]
        # The same thing for the url
        url = re.findall(r"\(.*?\)", s)[0][1:-1]
        result_list.append((alt_text, url))
    return result_list

def extract_markdown_links(text):
    splits = re.findall(r"(?<!!)\[.*?\]\(.*?\)", text)
    result_list = []
    for s in splits:
        # This weird expression below extracts just the alt text, without the surrounding brackets.
        link_text = re.findall(r"\[.*?\]", s)[0][1:-1]
        # The same thing for the url
        url = re.findall(r"\(.*?\)", s)[0][1:-1]
        result_list.append((link_text, url))
    return result_list

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    title = None
    for b in blocks:
        if block_to_blocktype(b) == BlockType.HEADING:
            heading = b.split(maxsplit=1)
            if len(heading[0]) == 1:
                title = heading[1]
    if title == None:
        raise Exception("A level 1 heading is required as the page title")
    return title

def markdown_to_blocks(text):
    splittext = text.split("\n\n")
    # Remove leading and trailing whitespace from each item
    splittext = list(map(lambda s: s.strip(), splittext))
    # Remove empty items that might appear when there are too many newlines between paragraphs
    splittext = list(filter(lambda s: len(s) > 0, splittext))
    return splittext

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            text = node.text
            while delimiter in text:
                # Find the first delimiter and separate the text that it delimits
                split_text = text.split(delimiter, maxsplit=2)
                if len(split_text) != 3:
                    # Every block should be closed, so delimiters should be paired in text
                    raise Exception("** tag not closed")
                
                if len(split_text[0]) > 0:
                    new_nodes.append(TextNode(split_text[0], TextType.PLAIN))
                new_nodes.append(TextNode(split_text[1], text_type))
                if len(split_text[2]) > 0:
                    text = split_text[2]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.PLAIN))

        else:
            # If the node is not just text, let's just append it.
            new_nodes.append(node)
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            text = node.text
            split_imgs = extract_markdown_images(text)
            while len(split_imgs) > 0:
                current = split_imgs.pop(0)
                alt_text = current[0]
                url = current[1]
                split_text = text.split(f"![{alt_text}]({url})", maxsplit=1)
                if len(split_text[0]) > 0:
                    new_nodes.append(TextNode(split_text[0], TextType.PLAIN))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                text = split_text[1]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.PLAIN))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            text = node.text
            split_links = extract_markdown_links(text)
            while len(split_links) > 0:
                current = split_links.pop(0)
                val = current[0]
                url = current[1]
                split_text = text.split(f"[{val}]({url})", maxsplit=1)
                if len(split_text[0]) > 0:
                    new_nodes.append(TextNode(split_text[0], TextType.PLAIN))
                new_nodes.append(TextNode(val, TextType.LINK, url))
                text = split_text[1]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.PLAIN))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    processed_list = [TextNode(text.replace("\n", " "), TextType.PLAIN)]
    processed_list = split_nodes_delimiter(processed_list, "**", TextType.BOLD)
    processed_list = split_nodes_delimiter(processed_list, "_", TextType.ITALIC)
    processed_list = split_nodes_delimiter(processed_list, "`", TextType.CODE)
    processed_list = split_nodes_image(processed_list)
    processed_list = split_nodes_link(processed_list)
    return processed_list
