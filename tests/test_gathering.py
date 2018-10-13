import pytest
import asyncio

from metrics import gatherapp


class OutputQueue:
    def __init__(self):
        self.result = []

    async def put(self, message):
        self.result.append(message)


class Producer:
    def __init__(self, queue, data):
        self._queue = queue
        self._data = data

    async def __call__(self):
        for item in self._data:
            if item is None:
                await self._queue.publish(item)
            else:
                b = gatherapp.Block(item)
                await self._queue.publish(b)


def test_single_producer():
    loop = asyncio.get_event_loop()
    in_queue = asyncio.Queue(loop=loop)

    out_queue = OutputQueue()

    notifier = gatherapp.SortBlocks(in_queue, out_queue)

    producer = Producer(in_queue, [3, 2, 5, 4, 1])

    loop.create_task(notifier())

    loop.run_until_complete(producer())

    loop.run_until_complete(notifier.stop())

    result = []

    for b in out_queue.result:
        result.append(b.block_num)

    assert [1, 2, 3, 4, 5] == result


def test_two_producers():
    loop = asyncio.get_event_loop()
    in_queue = asyncio.Queue(loop=loop)

    out_queue = OutputQueue()

    notifier = gatherapp.SortBlocks(in_queue, out_queue, producers_count=2)

    producer1 = Producer(in_queue, [6, 2, 4, 8, None])
    producer2 = Producer(in_queue, [3, 5, 7, 1, None])

    loop.create_task(notifier())
    loop.run_until_complete(asyncio.gather(producer1(), producer2()))
    loop.run_until_complete(notifier.stop())

    result = []

    for b in out_queue.result:
        result.append(b.block_num)

    assert [1, 2, 3, 4, 5, 6, 7, 8] == result

class Task:
    run = False

    async def __call__(self, name, count=5):
        self.run = True

        i = 0
        while self.run:
            if i == count:
                break
            i += 1
            print(name, i)
            await asyncio.sleep(1)

        self.run = False


def test_x():
    loop = asyncio.get_event_loop()
    in_queue = asyncio.Queue(loop=loop)

    producer = Task()
    consumer = Task()

    p = asyncio.ensure_future(producer("p "), loop=loop)
    c = asyncio.ensure_future(consumer("c ", 10), loop=loop)

    loop.run_until_complete(asyncio.gather(p, c))

    # loop.run_forever()
