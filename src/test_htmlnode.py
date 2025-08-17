import unittest

from htmlnode import HTMLNode

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

