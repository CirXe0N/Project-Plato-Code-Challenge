import json
import shutil
from pathlib import Path
from unittest import mock

from aiounittest import AsyncTestCase


from crawlers import Crawler
from scrapers import URLScraper


class CrawlerTest(AsyncTestCase):
    def setUp(self) -> None:
        self.crawler = Crawler(
            initial_url='https://www.example.test/',
            num_workers=1,
            out_path=Path('./out')
        )

    def test_add_to_queue(self) -> None:
        """
        Test the adding URL to the Queue.
        """

        urls = [
            # Valid URLS
            'https://www.example.test/',
            'https://www.example.test/a/',
            'https://www.example.test/a/b/',

            # Invalid URLS
            'https://www.otherexample2.test/',
            'https://www.otherexample3.test/',
        ]

        for url in urls:
            self.crawler._add_to_queue(url)

        self.assertEqual(self.crawler.queue.qsize(), 3)

    def test_add_to_visited_urls(self) -> None:
        """
        Test the adding URL to the visited list.
        """

        queue_url = 'https://www.example.test/a/'

        urls = [
            # Valid URLS
            'https://www.example.test/a/b/',
            'https://www.example.test/a/b/c',

            # Invalid URLS
            'https://www.example.test/',
            'https://www.otherexample2.test/',
            'https://www.otherexample3.test/',
        ]

        for url in urls:
            self.crawler._add_to_visited_urls(queue_url, url)

        self.assertEqual(len(self.crawler.visited_urls), 1)
        self.assertEqual(len(self.crawler.visited_urls[queue_url]), 3)

    def test_write_to_file(self) -> None:
        """
        Test writing output to a file.
        """

        self.crawler.visited_urls = {
            'https://www.example.test/': {
                'https://www.example.test/b/',
                'https://www.example.test/c/'
            },
            'https://www.example.test/b/': set()
        }

        self.crawler._write_to_file()

        with open('out/out.json', mode='r') as f:
            content = f.read()

        self.assertDictEqual(json.loads(content), self.crawler.visited_urls)

    @mock.patch.object(URLScraper, 'run')
    async def test_start_worker(self, mock_method) -> None:
        """
        Test the worker consuming the Queue.
        """
        mock_method.return_value = {'https://www.example.test/1'}
        queue_url = 'https://www.example.test/'
        self.crawler._add_to_queue(queue_url)

        await self.crawler._start_worker()

        self.assertEqual(self.crawler.queue.qsize(), 0)
        self.assertDictEqual(
            self.crawler.visited_urls,
            {
                'https://www.example.test/': {'https://www.example.test/1'},
                'https://www.example.test/1': {'https://www.example.test/1'},
            }
        )

    @mock.patch.object(URLScraper, 'run')
    async def test_run(self, mock_method) -> None:
        """
        Test the crawler with multiple workers.
        """
        mock_method.return_value = {
            'https://www.example.test/1',
            'https://www.example.test/2',
        }

        await self.crawler.run()

        with open('out/out.json', mode='r') as f:
            content = f.read()

        self.assertEqual(self.crawler.queue.qsize(), 0)
        self.assertEqual(len(self.crawler.visited_urls), 3)
        self.assertDictEqual(json.loads(content), self.crawler.visited_urls)

    @mock.patch.object(URLScraper, 'run')
    async def test_run_with_0_workers(self, mock_method) -> None:
        """
        Test the crawler with 0 workers.
        """
        mock_method.return_value = {
            'https://www.example.test/1',
            'https://www.example.test/2',
        }

        self.crawler.num_workers = 0

        with self.assertRaises(Exception) as context:
            await self.crawler.run()

        expected_msg = 'The number of workers must be higher than 1.'
        self.assertTrue(expected_msg in str(context.exception))

    def tearDown(self) -> None:
        path = Path('out')
        if path.exists():
            shutil.rmtree('out')
