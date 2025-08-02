from textnode import TextNode, TextType

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

