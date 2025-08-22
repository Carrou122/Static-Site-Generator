import unittest

from block_markdown import markdown_to_blocks, BlockType, block_to_block_type

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_no_blanks(self):
        md = """
This is **bolded** paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )
    def test_markdown_extra_blanks(self):
        md = """

This is **bolded** paragraph

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )
        
class TestBlockToBlocktype(unittest.TestCase):
    def test_block_to_blocktype(self):
        block = "### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_code_spaces(self):
        block = "``` This is code ```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_quote(self):
        block = ">This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- this is unordered list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        block = "1. this is ordered list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "this is test_paragraph"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_multi_quotes(self):
        block = "> line1\n> line2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_multi_unordered(self):
        block = "- item 1\n- item 2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_multi_ordered(self):
        block = "1. first\n2. second\n3. third"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_no_backcode(self):
        block = "``` this is fake code"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_multi_code(self):
        block = "```\nthis is code\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

