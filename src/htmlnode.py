class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        elif type(self.props) != dict:
            raise Exception("Props input must be a dictionary.")
        for key, value, in self.props.items():
            return f" {key}=\"{value}\""

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        elif self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    

    def to_html(self):
        if self.tag == None or "":
            raise ValueError("Invalid: no tag provided")
        elif self.children == None or "":
            raise ValueError("Invalid: no children provided")
        s = ""
        for child in self.children:
            s += child.to_html()
        return f"<{self.tag}>{s}</{self.tag}>"
            
        
        
        