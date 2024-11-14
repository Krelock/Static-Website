from enum import Enum
from htmlnode import LeafNode
from extract_markdown import  extract_markdown_images, extract_markdown_links



class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return(
            self.text_type == other.text_type 
            and self.text == other.text 
            and self.url == other.url
            )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        print(f"Original text to split: '{old_node.text}' using delimiter: '{delimiter}'")
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


        
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)

        if not images:
            new_nodes.append(old_node)
            continue
        else:
            remaining_text = old_node.text

            for image in images:
                image_alt = image[0]
                image_link = image[1]
                sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                
                if sections [0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                
                remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_links(old_node.text)

        if not images:
            new_nodes.append(old_node)
            continue
        else:
            remaining_text = old_node.text
            
            for image in images:
                image_alt = image[0]
                image_link = image[1]
                sections = remaining_text.split(f"[{image_alt}]({image_link})", 1)
                
                if sections [0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.LINK, image_link))
                
                remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes
    
    
        



