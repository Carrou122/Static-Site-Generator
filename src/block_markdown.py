
def markdown_to_blocks(markdown):
    block = markdown.strip().split("\n\n")
    f_block = list(filter(bool, map(str.strip, block)))
    return f_block
