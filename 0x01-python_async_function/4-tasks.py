#!/usr/bin/env python3
"""The basics of async"""

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Wait and return a list of delayed floats"""
    delays = [task_wait_random(max_delay) for _ in range(n)]
    return sorted([await delay for delay in delays])
