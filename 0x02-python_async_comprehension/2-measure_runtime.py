#!/usr/bin/env python3
""" Doc for module """
import asyncio

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ Measure total runtime of async_comprehension """
    start_time = asyncio.get_event_loop().time()
    await asyncio.gather(*[async_comprehension() for _ in range(4)])
    end = asyncio.get_event_loop().time() - start_time
    return end
