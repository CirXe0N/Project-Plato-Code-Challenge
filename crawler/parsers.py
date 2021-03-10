from html.parser import HTMLParser
from typing import NamedTuple


class HTMLLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag: str, attrs: NamedTuple) -> None:
        """
        Filter out the <a> tags and add the href value to the hrefs list.
        """

        if tag == 'a':
            href = dict(attrs).get('href')
            self.hrefs.append(href)
