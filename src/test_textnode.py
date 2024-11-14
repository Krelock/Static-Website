import unittest
from textnode import split_nodes_delimiter, split_nodes_image, split_nodes_links, text_to_textnodes

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_url_none(self):
        node = TextNode("This is a test node", TextType.BOLD)
        self.assertTrue(node.url == None)
 
class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        # Create a TextNode with some text that includes delimiters
        node = TextNode("This is **bold** and text", TextType.TEXT)
        old_nodes = [node]

        # Test splitting for bold text
        bold_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        
        
        assert len(bold_nodes) == 3
        assert bold_nodes[0].text == "This is "
        assert bold_nodes[1].text == "bold"
        assert bold_nodes[1].text_type == TextType.BOLD


    def test_split_nodes_images(self):
        nodes = TextNode(
            "This is text with an image ![alt text](https://example.com/image.jpg) and another ![second image](https://example.com/second.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([nodes])

        assert len(new_nodes) == 4

        assert new_nodes[0].text == "This is text with an image "
        assert new_nodes[0].text_type == TextType.TEXT

        assert new_nodes[1].text == "alt text"
        assert new_nodes[1].text_type == TextType.IMAGE
        assert new_nodes[1].url == "https://example.com/image.jpg"

        assert new_nodes[2].text == " and another "
        assert new_nodes[2].text_type == TextType.TEXT

        assert new_nodes[3].text == "second image"
        assert new_nodes[3].text_type == TextType.IMAGE
        assert new_nodes[3].url == "https://example.com/second.png"
   
   
    def test_split_nodes_images_none(self):
        nodes = TextNode(
            "this is text WITHOUT an image",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([nodes])


        self.assertEqual(new_nodes[0].text, "this is text WITHOUT an image")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertIsNone(new_nodes[0].url)
        
    
    def test_split_nodes_link(self):
        nodes = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )

        new_nodes = split_nodes_links([nodes])
        assert len(new_nodes) == 4  # Expecting 4 nodes after splitting

        assert new_nodes[0].text == "This is text with a link "
        assert new_nodes[0].text_type == TextType.TEXT

        assert new_nodes[1].text == "to boot dev"
        assert new_nodes[1].text_type == TextType.LINK
        assert new_nodes[1].url == "https://www.boot.dev"

        assert new_nodes[2].text == " and "
        assert new_nodes[2].text_type == TextType.TEXT

        assert new_nodes[3].text == "to youtube"
        assert new_nodes[3].text_type == TextType.LINK
        assert new_nodes[3].url == "https://www.youtube.com/@bootdotdev"

    def test_text_to_textnodes(self):
        nodes = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    
        new_nodes = text_to_textnodes(nodes)

        assert len(new_nodes) == 10

        assert new_nodes[0].text == "This is "
        assert new_nodes[0].text_type ==  TextType.TEXT

        assert new_nodes[1].text == "text"
        assert new_nodes[1].text_type == TextType.BOLD
        
        assert new_nodes[2].text == " with an "
        assert new_nodes[2].text_type == TextType.TEXT

        assert new_nodes[3].text == "italic"
        assert new_nodes[3].text_type == TextType.ITALIC
        
        assert new_nodes[4].text == " word and a "
        assert new_nodes[4].text_type == TextType.TEXT
        
        assert new_nodes[5].text == "code block"
        assert new_nodes[5].text_type == TextType.CODE

        assert new_nodes[6].text == " and an "
        assert new_nodes[6].text_type == TextType.TEXT

        assert new_nodes[7].text == "obi wan image"
        assert new_nodes[7].text_type == TextType.IMAGE
        assert new_nodes[7].url == "https://i.imgur.com/fJRm4Vk.jpeg"

        assert new_nodes[8].text == " and a "
        assert new_nodes[8].text_type == TextType.TEXT

        assert new_nodes[9].text == "link"
        assert new_nodes[9].text_type == TextType.LINK
        assert new_nodes[9].url == "https://boot.dev"

        


if __name__ == "__main__":
    unittest.main()

