import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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

class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is a test with multiple images ![image](https://i.imgur.com/Df1x7tq.jpeg) and ![imag2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/Df1x7tq.jpeg"), ("imag2", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_with_no_image(self):
        matches = extract_markdown_images(
            "This is a test"
        )
        self.assertListEqual([], matches)

    def test_with_both_image_n_links(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_with_empty_alt_text(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with multiple links [to boot dev](https://www.boot.dev) and [to google](https://www.google.com)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to google", "https://www.google.com")], matches)

    def test_with_no_links(self):
        matches = extract_markdown_links(
            "This is text with no links"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_images(self):
        matches = extract_markdown_links(
            "This is a test with link [to boot dev](https://www.boot.dev) and ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

if __name__ == "__main__":
    unittest.main()
