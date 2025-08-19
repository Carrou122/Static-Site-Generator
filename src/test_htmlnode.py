import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode
from main import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
#       assert node.props_to_html() == "" is the same as below
        self.assertEqual(node.props_to_html(), "")
        self.assertIsNone(node.props)
    
    def test_props_to_html_with_attributes(self):
        node = HTMLNode(props={"href": "https://a"})
        self.assertEqual(node.props_to_html(), ' href="https://a"')
    
    def test_props_to_html_multiple_attributes(self):
        node = HTMLNode(props={"href": "a", "target": "_blank"})
        result = node.props_to_html()
#       result should include both attributes, with a leading space
        self.assertTrue(result.startswith(" "))
        self.assertIn('href="a"', result)
        self.assertIn('target="_blank"', result)
#       should only have spaces between words (not doubled at the end)
        self.assertNotIn("  ", result)

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_empty_value(self):
        node = HTMLNode(props={"href": ""})
        self.assertEqual(node.props_to_html(), ' href=""')

    def test_eq_same_data(self):
        n1 = HTMLNode(tag="p", value="hi", props={"x": "y"})
        n2 = HTMLNode(tag="p", value="hi", props={"x": "y"})
        self.assertEqual(n1, n2)
    
    def test_eq_different_tag(self):
        n1 = HTMLNode(tag="p")
        n2 = HTMLNode(tag="div")
        self.assertNotEqual(n1, n2)

    def test_eq_nested(self):
        child1 = HTMLNode(tag="b", value="bold")
        child2 = HTMLNode(tag="b", value="bold")
        n1 = HTMLNode(tag="p", children=[child1])
        n2 = HTMLNode(tag="p", children=[child2])
        self.assertEqual(n1,n2)

class TestLeafNode(unittest.TestCase):
    def test_to_html_empty_dict(self):
        node = LeafNode('hi',tag=None,props={})
        self.assertEqual(node.to_html(), 'hi')

    def test_to_html_with_tag(self):
        node = LeafNode(tag="p", value="hi", props={})
        self.assertEqual(node.to_html(), '<p>hi</p>')

    def test_to_html_with_props(self):
        node = LeafNode(tag="p", value="hi", props={"x": "y"})
        self.assertEqual(node.to_html(), '<p x="y">hi</p>')

    def test_something_descriptive_to_html(self):
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_to_html_no_value(self):
        node = LeafNode(tag="a", value=None, props={})
        with self.assertRaises(ValueError): 
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span",value="child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode("span",[grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_no_tag(self):
        child_node = LeafNode(tag=None, value="child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_empty_list(self):
        parent_node = ParentNode("a", [])
        self.assertEqual(parent_node.to_html(), "<a></a>")

    def test_to_html_with_props(self):
        node = ParentNode("a", [LeafNode(tag="b", value="Click me")], {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev"><b>Click me</b></a>')

class TestMainFunction(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Test node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Test node")

    def test_italic(self):
        node = TextNode("Test node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Test node")

    def test_code(self):
        node = TextNode("Test node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Test node")

    def test_link(self):
        node = TextNode("Test node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"a")
        self.assertEqual(html_node.value, "Test node")
        self.assertEqual(html_node.props,{"href": "https://www.boot.dev"} )

    def test_image(self):
        node = TextNode("Test node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "Test node"})
    
    def test_exception(self):
        node = TextNode("Test node", "INVALID_TYPE")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
