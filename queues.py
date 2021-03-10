from asyncio import Queue


class UniqueQueue(Queue):
    def _init(self, maxsize: int) -> None:
        self._queue = set()

    def _put(self, item: object) -> None:
        self._queue.add(item)

    def _get(self) -> None:
        return self._queue.pop()
