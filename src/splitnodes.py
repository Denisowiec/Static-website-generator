from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images, extract_markdown_links

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
