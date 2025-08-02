from htmlnode import HTMLNode

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
    
