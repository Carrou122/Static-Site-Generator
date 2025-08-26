from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_list = []
        if self.props:
            for key, value in self.props.items():
                props_list.append(f'{key}="{value}"')
            return " " + " ".join(props_list)
        else:
            return ""

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        else:
            props_str = self.props_to_html()
            return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag error")
        if self.children is None:
            raise ValueError("No children error")
        else:
            child_list = []
            for child in self.children:
                child_list.append(child.to_html())
            child_str = "".join(child_list) 
            props_str = self.props_to_html()
            return f'<{self.tag}{props_str}>{child_str}</{self.tag}>'

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
