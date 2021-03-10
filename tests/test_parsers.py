from unittest import TestCase

from parsers import HTMLLinkParser


class HTMLLinkParserTest(TestCase):
    def setUp(self) -> None:
        self.parser = HTMLLinkParser()

    def test_parsing_and_retrieve_hrefs(self) -> None:
        """
        Test the retrieval of the various types of href values.
        """

        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
            <a href="https://www.example.test/">Link 1</a>
            <a href="https://www.example.test/index.html">Link 2</a>
            <a href="/index.html">Link 3</a>
            <a href="index.html">Link 4</a>
            <a href="#header1">Link 5</a>
            <a href="ftp://www.example.test/">Link 6</a>
            <a href="mailto:test@test.com">Link 7</a>
            <a href="javascript:alert('Hello');">Link 8</a>
            <a href="">Link 9</a>
            <a>Link 10</a>
        </body>
        </html>
        """

        self.parser.feed(html)

        self.assertListEqual(
            self.parser.hrefs,
            [
                'https://www.example.test/',
                'https://www.example.test/index.html',
                '/index.html',
                'index.html',
                '#header1',
                'ftp://www.example.test/',
                'mailto:test@test.com',
                "javascript:alert('Hello');",
                '',
                None
            ]
        )
