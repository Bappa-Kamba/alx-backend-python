#!/usr/bin/env python3
"""Basics of Async Comprehensions"""

import random
import asyncio
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator:
    """Coroutine that loops 10 times,
    each time asynchronously yields a random number between 0 and 10"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
