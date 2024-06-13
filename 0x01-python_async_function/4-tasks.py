#!/usr/bin/env python3
"""The basics of async"""

import asyncio

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> list:
    """Wait and return a list of delayed floats"""
    delays = [task_wait_random(max_delay) for _ in range(n)]
    return [await delay for delay in delays]


n = 5
max_delay = 6
print(asyncio.run(task_wait_n(n, max_delay)))
