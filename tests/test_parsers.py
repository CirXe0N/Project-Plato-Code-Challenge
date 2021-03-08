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

        assert len(self.parser.hrefs) == 10
        assert self.parser.hrefs[0] == 'https://www.example.test/'
        assert self.parser.hrefs[1] == 'https://www.example.test/index.html'
        assert self.parser.hrefs[2] == '/index.html'
        assert self.parser.hrefs[3] == 'index.html'
        assert self.parser.hrefs[4] == '#header1'
        assert self.parser.hrefs[5] == 'ftp://www.example.test/'
        assert self.parser.hrefs[6] == 'mailto:test@test.com'
        assert self.parser.hrefs[7] == "javascript:alert('Hello');"
        assert self.parser.hrefs[8] == ''
        assert self.parser.hrefs[9] is None
