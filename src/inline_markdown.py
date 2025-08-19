from textnode import TextNode, TextType
import re 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception('unmatched delimiter')
            for idx, part in enumerate(parts):
                if part:
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
