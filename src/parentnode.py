from htmlnode import HTMLNode

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

