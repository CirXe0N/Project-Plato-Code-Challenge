import asyncio
import json
import logging
from pathlib import Path

from crawler.queues import UniqueQueue
from crawler.scrapers import URLScraper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


class Crawler:
    def __init__(self, initial_url: str, out_path: Path, num_workers: int = 5):
        self.tasks = []
        self.visited_urls = {}
        self.num_workers = num_workers
        self.initial_url = initial_url
        self.queue = UniqueQueue()
        self.out_path = out_path

    def _add_to_queue(self, url: str) -> None:
        """
        Add URL to the queue to be crawled.
        """

        has_valid_start = url.startswith(self.initial_url)
        is_new = url not in self.visited_urls
        if has_valid_start and is_new:
            self.queue.put_nowait(url)

    def _add_to_visited_urls(self, queue_url: str, url: str) -> None:
        """
        Add found URL to list of the scraped URL.
        """
        if queue_url not in self.visited_urls:
            self.visited_urls[queue_url] = set()

        if url.startswith(self.initial_url):
            self.visited_urls[queue_url].add(url)

    def _write_to_file(self) -> None:
        """
        Write the visited URLs to the JSON file.
        """

        filepath = Path(self.out_path / 'out.json')
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with filepath.open('w') as file:
            for k, v in self.visited_urls.items():
                self.visited_urls[k] = list(v)
            file.write(json.dumps(self.visited_urls, indent=2))

    async def _start_worker(self, name):
        """
        Start worker to consume the Queue with URLs.
        """
        num_retries = 0

        while True:
            try:
                queue_url = self.queue.get_nowait()
                urls = URLScraper(url=queue_url).run()

                for url in urls:
                    self._add_to_visited_urls(queue_url, url)
                    self._add_to_queue(url)

                logging.info(f'{name} crawled URL: {queue_url}')
                self.queue.task_done()
                num_retries = False

            except asyncio.QueueEmpty:
                num_retries += 1

            finally:
                if num_retries > 3:
                    break

                await asyncio.sleep(1)

    async def run(self):
        """
        Run crawler to walk from the specified initial URL.
        """

        tasks = []

        if self.num_workers <= 0:
            raise ValueError('The number of workers must be higher than 1.')

        await self.queue.put(self.initial_url)

        for i in range(self.num_workers):
            name = f'Worker-{i + 1}'
            logging.info(f'Starting {name}')
            task = asyncio.create_task(self._start_worker(name=name))
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)

        self._write_to_file()

        logging.info(
            f'Crawled successfully! Open the file '
            f'"{self.out_path / "out.json"}" for the results.'
        )
