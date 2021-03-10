from unittest import TestCase, mock
from unittest.mock import MagicMock

from crawler.scrapers import URLScraper


class MockResponse:
    def __init__(self, body: bytes, status: int = 200):
        self.body = body
        self.status = status
        self.headers = {'content-type': 'text/html; charset=utf-8'}

    def read(self) -> bytes:
        return self.body


class URLScraperTest(TestCase):
    def setUp(self) -> None:
        self.scraper = URLScraper(url='https://www.example.test/')

    @mock.patch(
        'crawler.scrapers.urlopen',
        return_value=MockResponse(body=b'Test Body')
    )
    def test_GET_request(self, mock_urlopen: MagicMock) -> None:
        """
        Test a GET request to the specified URL.
        """

        response = self.scraper._make_get_request()

        mock_args = mock_urlopen.call_args.args

        self.assertEqual(mock_urlopen.call_count, 1)
        self.assertEqual(mock_args[0].full_url, 'https://www.example.test/')
        self.assertEqual(mock_args[0].method, 'GET')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.read().decode(), 'Test Body')

    @mock.patch('crawler.scrapers.urlopen')
    def test_run(self, mock_urlopen: MagicMock) -> None:
        """
        Test the retrieval of URL's from a HTML response.
        """

        mock_urlopen.return_value = MockResponse(
            body=b'''
            <a href="https://www.example.test/a/b/c/">Link 1</a>
            <a href="https://www.example.test/d/f/g/">Link 2</a>
            '''
        )

        hrefs = self.scraper.run()
        hrefs = list(hrefs)

        self.assertEqual(mock_urlopen.call_count, 1)
        self.assertListEqual(
            hrefs,
            [
                'https://www.example.test/a/b/c/',
                'https://www.example.test/d/f/g/'
            ]
        )
