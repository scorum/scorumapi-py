#!/usr/bin/env python3

import asyncio
import uvloop

import signal

from api import api
from api import async_api

from metrics import timeit


url = "http://127.0.0.1:8022"
url2 = "http://127.0.0.1:8023"


class AsyncScan:
    run = True

    async def scan(self, url: str, start: int, end: int):
        i = start
        limit = 100
        while self.run and i < end:
            ret = await async_api.get_blocks_history(url, i, limit)
            i += limit


class BlockingScan:
    run = True

    def scan(self, start: int, end: int):
        i = start
        limit = 100

        while self.run and i < end:
            api.get_blocks_history(url, i, limit)
            i += limit


@timeit
def async_scan(start, end):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    scanner = AsyncScan()

    def handler(signum, frame):
        scanner.run = False

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    loop.run_until_complete(scanner.scan(url, start, end))


@timeit
def async_scan2(start, end):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    scanner = AsyncScan()

    def handler(signum, frame):
        scanner.run = False

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    loop.run_until_complete(asyncio.gather(
        scanner.scan(url, start, end/2),
        scanner.scan(url2, end/2, end)))

    loop.close()

@timeit
def blocking_scan(start, end):
    scanner = BlockingScan()

    def handler(signum, frame):
        scanner.run = False

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    scanner.scan(start, end)


def main():
    start = 0
    end = 1000000

    async_scan(start, end)
    async_scan2(start, end)
    blocking_scan(start, end)


def get_one_block():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    scanner = AsyncScan()

    def handler(signum, frame):
        scanner.run = False

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    loop.run_until_complete(scanner.scan(url, 0, 1))


if __name__ == '__main__':
    # get_one_block()
    main()
