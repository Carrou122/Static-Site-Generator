import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_link


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


class TestSplit(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with link [to boot dev](https://www.boot.dev) and [to google](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to google", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_no_image(self):
        node = TextNode(
            "This is text with nothing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with nothing", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_link(self):
        node = TextNode(
            "This is text with nothing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with nothing", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_only_image_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_only_link_no_text(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_adjacent_links(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)[to google](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("to google", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_adjacent_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_image_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_start(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_before(self):
        node = TextNode(
            "text before ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_link_before(self):
        node = TextNode(
            "text before [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_empty_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [],
            new_nodes,
        )

    def test_non_text_node(self):
        node = TextNode("irrelevant", TextType.IMAGE, "http://img")
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [node],  # Should pass through unchanged
            new_nodes,
        )
    def test_malformed_markdown(self):
        node = TextNode("This is not actually an image ![alt](not a real url", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [node],  # The returned node list should be unchanged, as nothing validly split
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
