from http.client import HTTPResponse
from typing import Generator
from urllib.parse import urljoin, urldefrag
from urllib.request import Request, urlopen

from parsers import HTMLLinkParser


class URLScraper:
    default_headers = {
        'Accept': 'text/html',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) '
                      'Gecko/20100101 Firefox/86.0'
    }

    def __init__(self, url: str) -> None:
        self.url = url

    def _make_get_request(self) -> HTTPResponse:
        """
        Make a GET request to the specified URL.

        :return HTTPResponse
        """

        request = Request(
            url=self.url,
            method='GET',
            headers=self.default_headers
        )
        response = urlopen(request)
        return response

    def run(self) -> Generator:
        """
        Make a request to retrieve URL's from HTML responses.

        :return Generator
        """

        response = self._make_get_request()
        parser = HTMLLinkParser()
        parser.feed(response.read().decode())

        for href in parser.hrefs:
            path, _ = urldefrag(href)
            yield urljoin(self.url, path)
