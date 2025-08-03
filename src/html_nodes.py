from text_and_markdown import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        output = ""
        for tag, value in self.props.items():
            output = output + f' {tag}="{value}"'
        return output
    def __repr__(self):
        return f"\nHTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, value = None, props=None):
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag")
        if self.children == None:
            raise ValueError("No children")
        
        result = ""
        if self.props is not None:
            props = self.props_to_html()
            result += f"<{self.tag}{props}>"
        else:
            result += f"<{self.tag}>"

        for child in self.children:
            result += child.to_html()
        
        result += f"</{self.tag}>"
        return result

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag is None:
            return self.value
        
        if self.props is not None:
            props = self.props_to_html()
        else:
            props = ""
        
        # if there's no text value, make a self-closed tag
        if self.value is None:
            result = f"<{self.tag}{props} />"
        else:
            result = f"<{self.tag}{props}>{self.value}</{self.tag}>"
        
        return result
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("text_node has to be one of the TextType enum types")
        
def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    processed_blocks = list(map(block_to_parentnode, blocks))
    return ParentNode("div", processed_blocks)
    
def block_to_parentnode(block):
    block_type = block_to_blocktype(block)
    match block_type:
        case BlockType.PARAGRAPH:
            children = text_to_textnodes(block)
            if len(children) > 0:
                children_nodes = list(map(text_node_to_html_node, children))
                node = ParentNode("p", children_nodes)
            else:
                node = LeafNode("p", block)

        case BlockType.HEADING:
            # Number of hash symbols indicates the level of heading
            h_number = len(block.split(maxsplit=1)[0])
            # Remove the markdown formatting
            block = block.lstrip("# ")
            children = text_to_textnodes(block)
            if len(children) > 0:
                children_nodes = list(map(text_node_to_html_node, children))
                node = ParentNode(f"h{h_number}", children_nodes)
            else:
                node = LeafNode(f"h{h_number}", block)

        case BlockType.CODE:
            block = block.strip("```")
            block = block.strip("\n")
            child = LeafNode("code", block)
            node = ParentNode("pre", [child])
            
        case BlockType.QUOTE:
            lines = block.split("\n")
            lines = list(map(lambda x: x.lstrip("> "), lines))
            block = "\n".join(lines)
            children = text_to_textnodes(block)
            if len(children) > 0:
                children_nodes = list(map(text_node_to_html_node, children))
                node = ParentNode("blockquote", children_nodes)
            else:
                node = LeafNode("blockquote", block)

        case BlockType.UNORDERED_LIST:
            children = extract_list_elements(block, BlockType.UNORDERED_LIST)
            node = ParentNode("ul", children, None)
        case BlockType.ORDERED_LIST:
            children = extract_list_elements(block, BlockType.ORDERED_LIST)
            node = ParentNode("ol", children, None)
        case _:
            pass
    return node

def extract_list_elements(block, block_type):
    lines = block.split("\n")
    if block_type == BlockType.ORDERED_LIST:
        stripped_lines = list(map(lambda x: x.lstrip("1234567890. "), lines))
    elif block_type == BlockType.UNORDERED_LIST:
        stripped_lines = list(map(lambda x: x.lstrip("- "), lines))
    else:
        raise Exception("Not a list block!")
    
    list_items = []
    for l in stripped_lines:
        children = text_to_textnodes(l)
        if len(children) > 0:
            children = list(map(text_node_to_html_node, children))
            list_items.append(ParentNode("li", children))
        else:
            list_items.append(LeafNode("li", l))

    return list_items
