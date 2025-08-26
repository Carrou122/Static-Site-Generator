from enum import Enum
import re

def markdown_to_blocks(markdown):
    lines = markdown.splitlines()
    current = []
    blocks = []
    def is_heading(line):
        return re.match(r"^#{1,6}\s", line) is not None
    def is_unordered(line):
        return re.match(r"^\s*-\s", line) is not None
    def is_ordered(line):
        return re.match(r"\s*\d+.\s", line) is not None
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.strip() == "":
            if current:
                blocks.append("\n".join(current))
                current = []
            i += 1
            continue
        if is_heading(line):
            if current: 
                blocks.append("\n".join(current)) 
                current = []
            blocks.append(line)
            i += 1
            continue
        if is_unordered(line):
            if current:
                blocks.append("\n".join(current))
                current = []
            list_lines = []
            while i < n and is_unordered(lines[i]):
                list_lines.append(lines[i])
                i += 1
            blocks.append("\n".join(list_lines))
            continue
        if is_ordered(line):
            if current:
                blocks.append("\n".join(current))
                current = []
            list_lines = []
            while i < n and is_ordered(lines[i]):
                list_lines.append(lines[i])
                i += 1
            blocks.append("\n".join(list_lines))
            continue
        current.append(line)
        i += 1
    if current: 
        blocks.append("\n".join(current))

    return [b.strip() for b in blocks if b.strip()]

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

