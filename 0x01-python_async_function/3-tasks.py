#!/usr/bin/env python3
"""
Doc for thr module
"""
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int = 10) -> asyncio.Task:
    """ Doc for function """
    e_loop = asyncio.get_event_loop()
    return e_loop.create_task(wait_random(max_delay))
