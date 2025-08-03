from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "undordered list"
    ORDERED_LIST = "ordered_list"

def block_to_blocktype(single_block):
    # Check if it is heading
    test = re.findall(r"^#{1,6} ", single_block)
    if len(test) > 0:
        return BlockType.HEADING
    
    # Check if it is quote
    brackets = re.findall(r"(^|\n)> ", single_block)
    newlines = single_block.split("\n")
    if len(brackets) == len(newlines):
        return BlockType.QUOTE
    
    # Check if it is block code
    test = re.findall(r"^```|```$", single_block)
    if len(test) == 2:
        return BlockType.CODE
    
    # Check if it is an unordered list
    listitems = re.findall(r"(^|\n)- ", single_block)
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
