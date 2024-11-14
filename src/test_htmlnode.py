from htmlnode import HtmlNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import TextNode
from textnode import TextType
from textnode import text_node_to_html_node

import unittest


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        # Create an HTMLNode with some props
        node = HtmlNode(props={"href": "https://www.example.com", "target": "_blank"})
        
        # Check if props_to_html() returns the expected string
        expected = ' href="https://www.example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def  test_to_html(self):
        node = HtmlNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    

    def test_html_node(self):
        node = HtmlNode("h","THIS IS A TEST")
        node2 = "THIS IS A TEST"
        self.assertEqual(node.value, node2)



class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"

        self.assertEqual(node.to_html(), expected)
    
    def test_value_none(self):
        node = LeafNode("", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_tag_none(self):
        node = LeafNode(None,"Hi")
        node2 = "Hi"
        self.assertEqual(node.to_html(),node2)


class TestParentNode(unittest.TestCase):
    def test_error(self):
        node = ParentNode(tag = "a", children=None,  props=None)
        with self.assertRaises(ValueError):
            node.to_html()
            


    def test_main(self):
        node = ParentNode( 
            "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
            ]
        )
       
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        
        self.assertEqual(node.to_html(), expected)
    
class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("test test test", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value,"test test test")
if __name__ == "__main__":

    unittest.main()