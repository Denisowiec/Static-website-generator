from textnode import TextNode, TextType
from splitnodes import split_nodes_image, split_nodes_link
from splitnodesdelimiter import split_nodes_delimiter

def text_to_textnodes(text):
    processed_list = [TextNode(text, TextType.PLAIN)]
    processed_list = split_nodes_delimiter(processed_list, "**", TextType.BOLD)
    processed_list = split_nodes_delimiter(processed_list, "_", TextType.ITALIC)
    processed_list = split_nodes_delimiter(processed_list, "`", TextType.CODE)
    processed_list = split_nodes_image(processed_list)
    processed_list = split_nodes_link(processed_list)
    return processed_list
