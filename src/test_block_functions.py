from block_functions import markdown_to_blocks, block_to_block_type, block_to_htmlnode, markdown_to_html_node, text_to_children, extract_title

from htmlnode import HtmlNode
import unittest


class TestMarkDown(unittest.TestCase):
    def test_basic_blocks(self):
        markdown = "# Heading\n\nParagraph\n\n* List item"
        expected = ["# Heading", "Paragraph", "* List item"]
        
        self.assertEqual(markdown_to_blocks(markdown), expected)
    def test_empty(self):
        markdown = ""
        expected = []
        
        self.assertEqual(markdown_to_blocks(markdown),expected)
    def test_extra_lines(self):
        markdown = "# Heading\n\n\n\n\nParagraph\n\n\n\n\n* List item"
        expected = ["# Heading", "Paragraph", "* List item"]
        
        self.assertEqual(markdown_to_blocks(markdown), expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_empty(self):
        block = ""
        with self.assertRaises(ValueError):
            block_to_block_type(block)
    def test_heading(self):
        block = "### Heading"
        expected =  'heading'
        
        self.assertEqual(block_to_block_type(block), expected)
    def test_code(self):
        block = "``` magic code block ```"
        expected = 'code'
       
        self.assertEqual(block_to_block_type(block), expected)
    def test_quote(self):
        block = ">this is a magic quote"
        expected = 'quote'
        
        self.assertEqual(block_to_block_type(block), expected)
    def test_ordered_list(self):
        block = """1. Hello
        2. This
        3. is
        4. a
        5. test:)"""
        expected = 'ordered_list'
       
        self.assertEqual(block_to_block_type(block), expected)
    def test_paragraph(self):
        block = 'abby abbs is so gay it hurts'
        expected = 'paragraph'
        
        self.assertEqual(block_to_block_type(block), expected)

class TestBlockToHTMLNode(unittest.TestCase):
    def test_unordered_list(self):
        pass
        x = []
        expected = []

        self.assertEqual(x, expected)

    def test_ordered_list(self):
        pass
        x = []
        expected = []

        self.assertEqual(x, expected)

    def test_code(self):
        pass
        x = []
        expected = []

        self.assertEqual(x, expected)

    def test_heading(self):
        pass
        x = []
        expected = []

        self.assertEqual(x, expected)
    def test_paragraph(self):
        block = 'test test test'
        block_type = 'paragraph'
        html_node = block_to_htmlnode(block_type, block)
       
        
        assert html_node.tag == "p"
        assert html_node.value == None

        

class TestExtractMarkdownTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown_input = """# Heading 

        This is a paragraph."""
        expected = "Heading"
        self.assertEqual(extract_title(markdown_input), expected)
    
    def test_extract_weird_title(self):
        markdown_input = """helloooooooo
        
        
        
        rasrasr
        
        asrars
        
# This is a heading """
        

        expected = "This is a heading"
        self.assertEqual(extract_title(markdown_input), expected)

        
    
class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_paragraph_conversion(self):
        markdown = "This is a simple paragraph."
        html_node = markdown_to_html_node(markdown)
        
        # Check that the HTMLNode is a 'div' with one child
        assert html_node.tag == 'div'
        assert len(html_node.children) == 1

        # Check that the child is a 'p' element with correct text content
       
        assert html_node.children[0].tag == 'p'
        assert len(html_node.children[0].children) == 1
        
        assert html_node.children[0].children[0].value == "This is a simple paragraph."


    def test_multiple_blocks_conversion(self):
        markdown = """# Heading 1 \n\nThis is a simple paragraph."""  # Ensure there's a double newline separating blocks
        html_node = markdown_to_html_node(markdown)
        
        
        # Check that the HTMLNode is a 'div' with two children
        assert html_node.tag == 'div'
        assert len(html_node.children) == 2

        # Check the first child node is a heading
        assert html_node.children[0].tag == 'h1'
        assert len(html_node.children[0].children) == 1  # Adjusted expected children count
        assert html_node.children[0].children[0].value == "Heading 1"

        # Check the second child node is a paragraph
        assert html_node.children[1].tag == 'p'
        assert len(html_node.children[1].children) == 1  # Adjusted expected children count
        assert html_node.children[1].children[0].value == "This is a simple paragraph."





    def test_unordered_lists(self):
        markdown = "- Item 1\n- Item 2"
        expected_html_node = HtmlNode("div", None, [
            HtmlNode("ul", None, [
                HtmlNode("li", None, text_to_children("Item 1")),
                HtmlNode("li", None, text_to_children("Item 2"))
            ])
        ])
        # Call the function you're testing
        result_html_node = markdown_to_html_node(markdown)
        print(f"Result Node: {result_html_node}, Expected Node: {expected_html_node}")
        for result, expected in zip(result_html_node.children, expected_html_node.children):
            print(f"Result Child: {result}, Expected Child: {expected}")
        # Assert that the actual and expected nodes are the same
        assert result_html_node == expected_html_node

    def test_multiple_blocks(self):
        # Sample markdown containing a heading and a paragraph
        markdown_input = """# Heading 1

This is a paragraph."""

        # Expected structure in `HtmlNode` terms
        expected_html_node = HtmlNode("div", None, [
            HtmlNode("h1", None, text_to_children("Heading 1")),
            HtmlNode("p", None, text_to_children("This is a paragraph."))
        ])

        # Execute the function
        result_html_node = markdown_to_html_node(markdown_input)

        # Detailed comparison of each child to ensure it matches expectations
        self.assertEqual(result_html_node, expected_html_node, "Mismatch in markdown to HTML conversion for multiple blocks")

if __name__ == '__main__':
    unittest.main()