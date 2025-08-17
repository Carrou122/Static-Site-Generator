import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
