from itertools import count
from htmlnode import HtmlNode, ParentNode
from textnode import text_to_textnodes, text_node_to_html_node

import re

def markdown_to_blocks(markdown):   
    return [block.strip() for block in markdown.split('\n\n') if block.strip() != ""]


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def block_to_htmlnode(block_type, block):
    if block_type == 'quote':
        lines = block.split('\n')
        cleaned_lines = [line.lstrip('>').strip() for line in lines]
        cleaned_block = ' '.join(cleaned_lines)
        return ParentNode("blockquote",text_to_children(cleaned_block))
    elif block_type == 'unordered_list':
        items = block.split("\n")
        list_items = []
        
        for item in items:
            item_text = item[2:]
            li_node = ParentNode("li",text_to_children(item_text))
            list_items.append(li_node)
        
        return ParentNode("ul",list_items)
    elif block_type == 'ordered_list':
        items = block.split("\n")
        list_items = []
        
        for item in items:
            item_text = re.sub(r'^\d+\.\s+', '', item).strip()
            li_node = ParentNode("li",text_to_children(item_text))
            list_items.append(li_node)
        
        return ParentNode("ol", list_items)
    elif block_type == 'code':
        if not block.startswith("```") or not block.endswith("```"):
            raise ValueError("Invalid code block")
        text = block[4:-3]
        children = text_to_children(text)
        code = ParentNode("code", children)
        return ParentNode("pre", [code])
            

    elif block_type == 'heading':
        hash_count = block.count('#')
        block = block.lstrip("#").strip()
        
        return ParentNode(f"h{hash_count}", text_to_children(block))
    elif block_type == 'paragraph':
        return ParentNode("p", text_to_children(block))
    else:
        raise ValueError("Not a valid block type stupid")

    
def block_to_block_type(block):
    if block == "" or block == None:
        raise ValueError("Block can not be empty")
    elif re.match(r'^#{1,6}\s+\S.+', block):
        return 'heading'
    elif block.startswith("```") and block.endswith ("```"):
        return 'code'
    elif all(line.startswith('>') for line in block.split('\n')):
        return 'quote'
    elif all(line.startswith('* ') or line.startswith('-')for line in block.split('\n')):
        return 'unordered_list'
    elif all(re.match(r'^\d+\.\s+', line.strip()) for line in block.split('\n')):
        return 'ordered_list'
    else:
        return 'paragraph'
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    list_of_html_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        list_of_html_nodes.append(block_to_htmlnode(type, block))

    return ParentNode("div", list_of_html_nodes)

def extract_title(markdown):
    split_markdown = markdown.split('\n')
    for text in split_markdown:
        if text.startswith("# "):
            text = text.replace('# ', '')
            return text.strip()
            
    raise Exception("Must have a title")

