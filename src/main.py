from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    if TextType.TEXT == text_node.text_type:
        return LeafNode(text_node.text, None)
    elif TextType.BOLD == text_node.text_type:
        return LeafNode(text_node.text, "b")
    elif TextType.ITALIC == text_node.text_type:
        return LeafNode(text_node.text, "i")
    elif TextType.CODE == text_node.text_type:
        return LeafNode(text_node.text, "code")
    elif TextType.LINK == text_node.text_type:
        return LeafNode(text_node.text, "a", {"href": text_node.url})
    elif TextType.IMAGE == text_node.text_type:
        return LeafNode("","img", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("TextType not recognised.")

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

main()
