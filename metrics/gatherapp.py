import json
import sys
import os
import signal
import asyncio
import signal
import logging
import functools
import math

from nats.aio.client import Client as NATS
from nats.aio.client import DEFAULT_MAX_PAYLOAD_SIZE
from nats.aio.errors import ErrMaxPayload, ErrConnectionClosed, ErrTimeout, ErrNoServers


from events import Events


from api import async_api

from metrics import timeit

#{
# "previous":"0000000137294bccbe526347f88fd54b8aa11a06",
# "block_id":"0000000244c06ea3266f6122a2e4c5201eccd14e",
# "witness_signature":"1f680668b25123a967d099a656eba7288822d70510cd9b57338ba1cfe577c9d48a4b46246752d44c32b2a158a580087aee52cecc46db5413f104ff86be8fb35626",
# "signing_key":"SCR6MmnQsDm6e8toRYXcwDdpQnmAeAdG8VuMzX6DGvk9ozWxoLeFy",
# "transaction_ids":[],
# "timestamp":"2018-03-23T14:15:06",
# "witness":"scorumwitness1",
# "transaction_merkle_root":"0000000000000000000000000000000000000000",
# "transactions":[],
# "extensions":[],"
# signatures":null}}


API_LIMIT = 100


# class Task:
#     def __init__(self, start, stop, url=""):
#         self.start = start
#         self.stop = stop
#         self.url = url
#
#     def __str__(self):
#         return "%d %d %s" % (self.start, self.end, self.url)

def create_schedule(start, end, hosts, limit=API_LIMIT):
    assert start > 0
    assert end > start
    assert limit > 0
    assert len(hosts) > 0

    total = end - start

    number_of_queries = int(math.ceil(total / limit))
    number_of_workers = min(number_of_queries, len(hosts))

    schedule = dict()

    worker = 0
    s = start

    while s < end:

        url = hosts[worker]

        if url not in schedule:
            schedule[url] = []

        schedule[url].append((s, s + limit))

        s += limit

        worker += 1

        if worker == number_of_workers:
            worker = 0

    return schedule


def get_range_for_runners(start_block, end_block, hosts, limit=API_LIMIT):
    assert end_block > start_block

    result = list()
    total_blocks = end_block - start_block + 1

    number_of_queries = max(1, int(math.ceil(total_blocks / limit)))
    number_of_workers = min(number_of_queries, len(hosts))

    blocks_per_reader = int(total_blocks / number_of_workers)

    assert blocks_per_reader > 0

    for i in range(number_of_workers - 1):
        result.append((start_block, start_block + blocks_per_reader, hosts[i]))
        start_block += blocks_per_reader

    result.append((start_block, end_block, hosts[-1]))

    return result


class Block:
    # timestamp = datetime.datetime.timestamp()
    # block_num = 0
    # previous = ""
    # block_id = ""
    # witness_signature = ""
    # signing_key = ""
    # transaction_ids = []
    # witness = ""
    # transaction_merkle_root = ""
    # # transactions = []
    # operations = []
    # extensions = []
    # signatures = []

    def __init__(self, data=None):
        self.block_num = data["block_num"]
        self.data = data

    def from_json(self, data):
        self.block_num = data["block_num"]
        self.data = data

        return self

    def __str__(self):
        return '{"block_num": %d}' % self.block_num

    def __bytes__(self):
        return bytes(json.dumps(self.data), 'utf-8')


class Reader2:
    def __init__(self, url, tasks, method):
        self._url = url
        self._tasks = tasks
        self._current_task = 0
        self._method = method

    async def get_next(self):
        start, end = self._tasks[self._current_task]

        response = await self._method(start, end, 100)

        if response is None:
            return []

        self._current_task += 1

        if self._current_task == len(self._tasks):
            self._current_task = 0
            self._tasks = None

        blocks = json.loads(response)["result"]

        return [Block(b) for b in blocks]


class Reader:
    def __init__(self, url, start, end, limit=API_LIMIT):
        assert start > 0
        assert end > 0
        assert start < end, "start=%d end=%d" % (start, end)

        self._logger = logging.getLogger('blocks_reader')

        self._url = url
        self._current = start
        self._end = end
        self._limit = limit

    def current(self):
        return self._current

    async def get_next(self):
        limit = min(self._end - self._current, self._limit)

        response = await async_api.get_blocks(self._url, self._current, limit)

        if response is None:
            return []

        blocks = json.loads(response)["result"]

        if len(blocks) != limit:
            self._logger.error("len(blocks) != limit, %d %d" % (len(blocks), limit))

        self._current += limit

        return [Block(b) for b in blocks]


class BlocksReader:
    def __init__(self):
        self._run = False

    async def __call__(self, queue: asyncio.Queue, url: str, start: int, end=sys.maxsize, step=API_LIMIT):

        reader = Reader(url, start, end, step)

        self._run = True

        while self.is_running() and reader.current() < end:
            blocks = await reader.get_next()

            if len(blocks) > 0:
                for b in blocks:
                    await queue.put(b)

        self._run = False

    def is_running(self):
        return self._run

    async def stop(self):
        self._run = False


class SortBlocks:
    def __init__(self, in_queue, mq=None, start=1):
        self._logger = logging.getLogger('sort_blocks')

        self._in_queue = in_queue
        self._mq = mq

        self._buffer = dict()

        self._next_block_num = start

        self._run = False

    def is_there_block_for_push(self):
        return True if self._next_block_num in self._buffer else False

    def _get_next_block(self):
        b = self._buffer.get(self._next_block_num)
        self._buffer.pop(self._next_block_num)
        self._next_block_num += 1

        return b

    async def stop(self):
        self._run = False
        await self._in_queue.put(None)

    async def __call__(self):
        self._run = True

        while self._run or self.is_there_block_for_push():
            block = await self._in_queue.get()

            if block is not None:

                if block.block_num < self._next_block_num:
                    raise Exception("Duplicate block")

                if block in self._buffer:
                    raise Exception("this block already in queue")

                self._buffer[block.block_num] = block

                while self.is_there_block_for_push():
                    block = self._get_next_block()

                    if block.block_num % 10000 == 0:
                        self._logger.info("synced %d blocks" % block.block_num)

                    payload = bytes(block)

                    try:
                        await self._mq.publish("block.%d" % block.block_num, payload)
                    except ErrMaxPayload as e:
                        self._logger.error(e)
                        self._logger.error("block:%d payload_size:%d max_payload:%d" % (block.block_num,
                                                                                        len(payload),
                                                                                        self._mq.max_payload))
                        raise e

        self._run = False


class OutputQueue:
    def __init__(self):
        self._logger = logging.getLogger('output_queue')
        self.counter = 0
        self.previous = 0

    async def publish(self, message):
        if message.block_num % 10000 == 0:
            self._logger.info("synced %d blocks" % message.block_num)

        if self.previous + 1 != message.block_num:
            self._logger.error("previous + 1 != next")

        self.previous = message.block_num
        self.counter += 1


class Gathering:
    def __init__(self, loop, mq, hosts):
        self._logger = logging.getLogger('gathering')

        self.readers = list()
        self.hosts = hosts
        self.mq = mq
        self.loop = loop

    def create_blocks_readers(self, schedule):
        self.readers = [BlocksReader() for _ in range(count)]

    def create_reading_tasks(self, queue, start, stop, hosts):
        jobs = get_range_for_runners(start, stop, hosts)

        schedule = create_schedule(start, stop, hosts)

        self.create_blocks_readers(schedule
                                   )

        tasks = list()
        for i in range(len(jobs)):
            s, e, u = jobs[i]
            tasks.append(self.readers[i](queue, u, s, e))

        return tasks

    def _set_signal_handler(self):
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.loop.add_signal_handler(sig, lambda: asyncio.ensure_future(self.stop_handler(), loop=self.loop))

    async def stop_handler(self):
        for s in self.readers:
            await s.stop()

    async def __call__(self, start, stop):
        queue = asyncio.Queue(loop=self.loop)

        sort_blocks = SortBlocks(queue, self.mq, start)

        blocks_reading_tasks = self.create_reading_tasks(queue, start, stop, self.hosts)

        blocks_sorting_task = self.loop.create_task(sort_blocks())

        await asyncio.gather(*blocks_reading_tasks)

        await asyncio.gather(sort_blocks.stop(), blocks_sorting_task)

        # self._logger.info("gathered %d blocks", self.service_queue.counter)

        self.readers.clear()


async def get_last_block(url):
    data = await async_api.get_dgp(url)
    return data["last_irreversible_block_num"], data["time"], data["head_block_number"]


class GatherApp:
    def __init__(self, loop, hosts):
        self._logger = logging.getLogger('gather_app')
        self._hosts = hosts
        self._run = False
        self._loop = loop

        # self._mq = OutputQueue()
        self._mq = NATS()

        self._gathering = Gathering(loop, self._mq, self._hosts)

    async def stop(self):
        self._logger.info("signal received.")
        self._logger.info("stop service.")
        self._run = False
        await self._gathering.stop_handler()
        await self._mq.close()

    async def run(self):
        self._run = True

        await self._mq.connect("127.0.0.1:4222", loop=self._loop, connect_timeout=1, max_reconnect_attempts=1)

        self._logger.info("connected to mq.")

        last_irreversible_block_num, head_block_time, _ = await get_last_block(self._hosts[0])
        start = 1

        self._logger.info("gathering from %d to %d" % (start, last_irreversible_block_num))

        await self._gathering(start, last_irreversible_block_num)

        start = last_irreversible_block_num

        while self._run:

            last_irreversible_block_num, head_block_time, _ = await get_last_block(self._hosts[0])

            self._logger.info("syncing from %d to %d" % (start, last_irreversible_block_num))

            if last_irreversible_block_num > start:
                await self._gathering(start, last_irreversible_block_num)
                start = last_irreversible_block_num

            if self._run:
                await asyncio.sleep(18)

        self._run = False

        await self._mq.close()


@timeit
def main_gathering():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-6s %(name)-12s %(message)s')

    hosts = ["http://127.0.0.1:8022", "http://127.0.0.1:8023"]

    loop = asyncio.get_event_loop()

    app = GatherApp(loop, hosts)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.ensure_future(app.stop(), loop=loop))

    loop.run_until_complete(app.run())


if __name__ == "__main__":
    main_gathering()
