import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("text", TextType.BOLD)
        node2 = TextNode("text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_url(self):
        node = TextNode("a link", TextType.LINK, url="http://example.com")
        self.assertIsNotNone(node.url)

    def test_url_is_none(self):
        node = TextNode("not a link", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_url_difference_not_equal(self):
        node1 = TextNode("link", TextType.LINK, url="http://example.com")
        node2 = TextNode("link", TextType.LINK, url="http://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_url_eq(self):
        node1 = TextNode("link", TextType.LINK, url="http://example.com")
        node2 = TextNode("link", TextType.LINK, url="http://example.com")
        self.assertEqual(node1, node2)

class TestDelimiter(unittest.TestCase):
    def test_delimiter_code(self):
        nodes = [TextNode("This is `code` and `more code`", TextType.TEXT)]
        self.assertEqual(
        split_nodes_delimiter(nodes, "`", TextType.CODE),
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
        ])
    
    def test_delimiter_even(self):
        nodes = [TextNode("This is `code and `more code`", TextType.TEXT)]
        with self.assertRaises(Exception): 
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_delimiter_none(self):
        nodes = [TextNode("This is code and more code", TextType.TEXT)]
        self.assertEqual(
        split_nodes_delimiter(nodes, "`", TextType.CODE),
        [TextNode("This is code and more code", TextType.TEXT)]
        )

if __name__ == "__main__":
    unittest.main()
