from aiounittest import AsyncTestCase

from crawler.queues import UniqueQueue


class UniqueQueueTest(AsyncTestCase):
    def setUp(self) -> None:
        self.queue = UniqueQueue()

    async def test_put_different_items(self) -> None:
        """
        Test the adding of different items.
        """

        await self.queue.put('abc1')
        await self.queue.put('abc2')

        self.assertEqual(self.queue.qsize(), 2)

    async def test_put_same_items(self) -> None:
        """
        Test the adding of the same items.
        """

        await self.queue.put('abc1')
        await self.queue.put('abc1')

        self.assertEqual(self.queue.qsize(), 1)

    async def test_get_item(self) -> None:
        """
        Test the retrieval of an item from the Queue.
        """

        await self.queue.put('abc1')
        await self.queue.put('abc2')

        await self.queue.get()

        self.assertEqual(self.queue.qsize(), 1)
