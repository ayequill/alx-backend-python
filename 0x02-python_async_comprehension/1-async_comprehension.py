#!/usr/bin/env python3
""" Doc for module """
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """ Doc for function """
    return [val async for val in async_generator()]
