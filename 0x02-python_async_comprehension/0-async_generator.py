#!/usr/bin/env python3
"""Basics of Async Comprehensions"""

import random
import asyncio
from typing import AsyncGenerator, Any


async def async_generator() -> AsyncGenerator[float, Any]:
    """Generate a random number"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
