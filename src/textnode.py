import re

from leafnode import LeafNode


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


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


# @input_value_printer
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)
        if len(parts) == 1:
            if len(old_nodes) == 1:
                raise ValueError("Missing delimiter")
            new_nodes.append(old_node)
            continue
            # raise ValueError("Missing delimiter")
        if len(parts) == 2:
            raise ValueError("Invalid Markdown syntax")
        for i in range(0, len(parts)):
            if i == 0 or i % 2 == 0:
                new_nodes.append(TextNode(parts[i], text_type_text))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        image_tups = extract_markdown_images(old_node.text)
        if len(image_tups) == 0:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        for i in range(0, len(image_tups)):
            image_tup = image_tups[i]
            parts = current_text.split(
                f"![{image_tup[0]}]({image_tup[1]})")
            new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(
                TextNode(image_tup[0], text_type_image, image_tup[1]))
            current_text = parts[1]
        if len(current_text) > 0:
            new_nodes.append(TextNode(current_text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
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


def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    bold_nodes = split_nodes_delimiter(
        [node], "**", text_type_bold)
    italic_nodes = split_nodes_delimiter(
        bold_nodes, "*", text_type_italic)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", text_type_code)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)

    return link_nodes


def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks


def extract_markdown_headings(text):
    matches = re.findall(r"^(#{1,6}\s)(.*)", text)
    return matches


def extract_markdown_code_blocks(text):
    matches = re.findall(r"^(```)(.*)(```)", text)
    return matches


def extract_markdown_quote_line(text):
    matches = re.findall(r"^(>)(.*)", text)
    return matches


def extract_markdown_ul_line(text):
    matches = re.findall(r"^(-|\*)(.*)", text)
    return matches

def extract_markdown_ol_line(text):
    matches = re.findall(r"^(\d)\.\s(.*)", text)
    return matches


def block_to_block_type(block):
    lines = block.split("\n")

    headings = extract_markdown_headings(block)
    if headings and len(headings[0]) == 2:
        return block_type_heading
    code_blocks = extract_markdown_code_blocks(block)
    if code_blocks and len(code_blocks[0]) == 3:
        return block_type_code

    num_quote_lines = 0
    for line in lines:
        quote_line = extract_markdown_quote_line(line)
        if quote_line and len(quote_line[0]) == 2:
            num_quote_lines += 1
    if num_quote_lines == len(lines):
        return block_type_quote

    num_ul_lines = 0
    for line in lines:
        ul_line = extract_markdown_ul_line(line)
        if ul_line and len(ul_line[0]) == 2:
            num_ul_lines += 1
    if num_ul_lines == len(lines):
        return block_type_unordered_list

    # check if numbers are incrementing properly
    num_ol_lines = 0
    last_num = 0
    increment = False
    for line in lines:
        ol_line = extract_markdown_ol_line(line)
        if ol_line and len(ol_line[0]) == 2:
            current_num = int(ol_line[0][0])
            if current_num == last_num + 1:
                last_num = current_num 
                increment = True
                num_ol_lines += 1
            else:
                increment = False
                break
    if increment:
        if num_ol_lines == len(lines):
            return block_type_ordered_list
    return block_type_paragraph
