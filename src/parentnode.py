from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None or not children:
            raise ValueError("ParentNode must have children")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.children:
            raise ValueError("ParentNode must have children")

        children_html = "" 
        for child in self.children:
            print(f"ParentNode to_html child: {child}")
            children_html += child.to_html()
        return  f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
