import re
from textnode import TextNode, TextType

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