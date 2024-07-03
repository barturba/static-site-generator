import re
from leafnode import LeafNode


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text=None, text_type=None, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(node):
    match node.text_type:
        case "text":
            return LeafNode(None, node.text)
        case "bold":
            return LeafNode("b", node.text)
        case "italic":
            return LeafNode("i", node.text)
        case "code":
            return LeafNode("code", node.text)
        case "link":
            return LeafNode("a", node.text, None, {"href": node.url})
        case "image":
            return LeafNode("img", "", None, {"src": node.url, "alt": node.text})
        case _:
            raise ValueError("Invalid text_type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)

        parts = node.text.split(delimiter)
        if len(parts) == 1:
            raise ValueError("Missing delimiter")
        if len(parts) == 2:
            raise ValueError("Invalid Markdown syntax")

        counter = 1
        for part in parts:
            if part:
                if counter % 2 == 0:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part, text_type_text))
                counter += 1

        return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
        if not node.text:
            continue

        original_text = node.text
        for image_tup in images:
            split_string = f"![{image_tup[0]}]({image_tup[1]})"
            split_text = original_text.split(
                f"![{image_tup[0]}]({image_tup[1]})", 1)
            new_nodes.append(TextNode(split_text[0], text_type_text))

            new_nodes.append(
                TextNode(image_tup[0], text_type_image, image_tup[1]))

            original_text = split_text[1]
        if original_text:
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
        if not node.text:
            continue

        original_text = node.text
        for link_tup in links:
            split_text = original_text.split(
                f"[{link_tup[0]}]({link_tup[1]})", 1)
            new_nodes.append(TextNode(split_text[0], text_type_text))

            new_nodes.append(
                TextNode(link_tup[0], text_type_link, link_tup[1]))

            original_text = split_text[1]
        if original_text:
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes
