import unittest
from extractmarkdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    def test_images(self):
        teststring = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(teststring)
        self.assertEqual(result, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
    def test_images_with_urls(self):
        teststring = "[A link in the beginning](http://wp.pl). This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), also: a [link](http://boot.dev)."
        result = extract_markdown_images(teststring)
        self.assertEqual(result, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
    def test_links_with_images(self):
        teststring = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), also: a [link](http://boot.dev)."
        result = extract_markdown_links(teststring)
        self.assertEqual(result, [('link', 'http://boot.dev')])
    def test_links_with_images_harder(self):
        teststring = "[A link in the beginning](http://wp.pl). This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), also: a [link](http://boot.dev)."
        result = extract_markdown_links(teststring)
        self.assertEqual(result, [('A link in the beginning', 'http://wp.pl'),('link', 'http://boot.dev')])

        