from enum import Enum
import re

def markdown_to_blocks(markdown):
    block = markdown.strip().split("\n\n")
    f_block = list(filter(bool, map(str.strip, block)))
    return f_block

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    lines = block.splitlines()
    if len(lines) >= 2 and lines[0].strip() == "```" and lines [-1].strip() == "```":
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{idx}. ") for idx, line in enumerate(lines, 1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

