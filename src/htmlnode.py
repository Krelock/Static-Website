
class HtmlNode():
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
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        return f"{self.tag},{self.value},{self.children},{self.props}"
    def __eq__(self,other):
        if not isinstance(other, HtmlNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children)


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
 

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    



class ParentNode(HtmlNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Object must have a tag")
        if not self.children:
            raise ValueError("Object must have at least one child")
        
        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result
                


