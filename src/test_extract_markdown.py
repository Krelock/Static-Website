import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links



class TestExtract(unittest.TestCase):
    def test_images(self):
        node = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg")
        node2 = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg")

        self.assertEqual(node,node2)
    
    def test_links(self):
        node = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        node2 = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")

        self.assertEqual(node,node2)