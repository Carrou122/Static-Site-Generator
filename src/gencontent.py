from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from block_markdown import *
from inline_markdown import text_to_children


def extract_title(markdown):
    for i in markdown.split('\n'):
        if i.startswith('# '):
            return i[2:].strip()
    raise Exception('No title found.')

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}.')
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    with open(dest_path, "w") as f:
        f.write(final_html)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_list = []
    for block in blocks:
        tblock = block_to_block_type(block)
        i = convert_block_to_html_node(block, tblock)
        block_list.append(i)
    hlist = ParentNode("div", children=block_list)
    return hlist


def convert_block_to_html_node(block, block_type):
    if block_type == BlockType.QUOTE:
        tchild = text_to_children(block[2:])
        return ParentNode("blockquote", children=tchild)
    if block_type == BlockType.PARAGRAPH:
        lines = block.splitlines()
        trimmed = [l.strip() for l in lines if l.strip() != ""]
        if not trimmed:
            return ParentNode("p", children=[])
        text = trimmed[0]
        for nxt in trimmed[1:]:
            if text and text[-1] in ".!?":
                text += nxt
            else:
                text += " " + nxt
        tchild = text_to_children(text)
        return ParentNode("p", children=tchild)
    if block_type == BlockType.HEADING:
        line =block.splitlines()[0]
        count = 0
        for ch in line:
            if ch == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and line[count] == " ":
            tchild = text_to_children(line[count + 1:])
            return ParentNode(f"h{count}", children=tchild)
    if block_type == BlockType.UNORDERED_LIST:
        iblock = block.split("\n")
        uo_list = []
        for eblock in iblock:
            uo_list.append(ParentNode("li", children=text_to_children(eblock[2:])))
        return ParentNode("ul", children=uo_list)
    if block_type == BlockType.ORDERED_LIST:
        iblock = block.split("\n")
        o_list = []
        for eblock in iblock:
            o_list.append(ParentNode("li", children=text_to_children(eblock.split(". ")[1])))
        return ParentNode("ol", children=o_list)
    if block_type == BlockType.CODE:
        ctext = block[4:len(block)-3]
        chtml = text_node_to_html_node(TextNode(ctext, TextType.TEXT))
        tchild = ParentNode("code", children=[chtml])
        return ParentNode("pre", children=[tchild])
    raise Exception("Invalid block type")



