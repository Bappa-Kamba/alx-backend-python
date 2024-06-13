#!/usr/bin/env python3
"""The basics of async"""

from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Wait and return a list of delayed floats"""
    delays = [wait_random(max_delay) for _ in range(n)]
    return sorted([await delay for delay in delays])
