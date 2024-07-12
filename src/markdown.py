from htmlnode import HTMLNode, ParentNode
from markdown_blocks import block_to_block_type, markdown_to_blocks
from textnode import text_to_textnodes


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes_children = []
    for block in blocks:
        print(f"block: {block}")
        node_tag = ""
        if block_to_block_type(block) == block_type_heading:
            if block.startswith("# "):
                node_tag = "h1"
            elif block.startswith("## "):
                node_tag = "h2"
            elif block.startswith("### "):
                node_tag = "h3"
            elif block.startswith("#### "):
                node_tag = "h4"
            elif block.startswith("##### "):
                node_tag = "h5"
            elif block.startswith("###### "):
                node_tag = "h6"
        elif block_to_block_type(block) == block_type_paragraph:
            node_tag = "p"
        elif block_to_block_type(block) == block_type_code:
            node_tag = "code"
        elif block_to_block_type(block) == block_type_quote:
            node_tag = "quote"
        elif block_to_block_type(block) == block_type_ulist:
            node_tag = "ul"
        elif block_to_block_type(block) == block_type_olist:
            node_tag = "ol"
        children = text_to_children(block)
        block_nodes_children.append(HTMLNode(node_tag, children))
    node = ParentNode("div", block_nodes_children)
    return node


def text_to_children(text):
    ## returns a list of htmlnodes using previously created functions
    print("text_to_children:")
    return text_to_textnodes(text)

    # match node.text_type:
    #     case "text":
    #         return LeafNode(None, node.text)
    #     case "bold":
    #         return LeafNode("b", node.text)
    #     case "italic":
    #         return LeafNode("i", node.text)
    #     case "code":
    #         return LeafNode("code", node.text)
    #     case "link":
    #         return LeafNode("a", node.text, None, {"href": node.url})
    #     case "image":
    #         return LeafNode("img", "", None, {"src": node.url, "alt": node.text})
    #     case _:
    #         raise ValueError("Invalid text_type")
