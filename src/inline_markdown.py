from textnode import TextNode, TextType
import re 
from htmlnode import text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts) < 3:
                node_list.append(node)
                continue
            if len(parts) % 2 == 0:
                raise Exception("unmatched delimiter")
            for idx, part in enumerate(parts):
                if part == "":
                    continue
                if idx % 2 == 0:
                    node_list.append(TextNode(part, TextType.TEXT))  
                else:
                    node_list.append(TextNode(part, text_type))
        else:
            node_list.append(node)
    return node_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes):
    node_list = []
    for node in old_nodes:
        working_text = node.text
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        while extract_markdown_images(working_text):
            alt, url = extract_markdown_images(working_text)[0]
            alt_url = f"![{alt}]({url})"
            before, after = working_text.split(alt_url, 1)
            if before:
                node_list.append(TextNode(before, TextType.TEXT))
            node_list.append(TextNode(alt, TextType.IMAGE, url))
            working_text = after
        if working_text:
            node_list.append(TextNode(working_text, TextType.TEXT))
    return node_list

def split_nodes_link(old_nodes):
    node_list = []
    for node in old_nodes:
        working_text = node.text
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        while extract_markdown_links(working_text):
            alt, url = extract_markdown_links(working_text)[0]
            alt_url = f"[{alt}]({url})"
            before, after = working_text.split(alt_url, 1)
            if before:
                node_list.append(TextNode(before, TextType.TEXT))
            node_list.append(TextNode(alt, TextType.LINK, url))
            working_text = after
        if working_text:
            node_list.append(TextNode(working_text, TextType.TEXT))
    return node_list

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_children(text):
    textnode_list = text_to_textnodes(text)
    html_node_list = []
    for textnode in textnode_list:
        html_node_list.append(text_node_to_html_node(textnode))
    return html_node_list

