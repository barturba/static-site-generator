from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None or not isinstance(children, list) or not children:
            raise ValueError(
                "ParentNode must have children and children must be a list")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.children:
            raise ValueError("ParentNode must have children")
        if self.children is ParentNode:
            return self.children.to_html()

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
