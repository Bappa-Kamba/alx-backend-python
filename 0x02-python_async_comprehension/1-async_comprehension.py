#!/usr/bin/env python3
"""Async Comprehensions"""

from typing import Generator, Any

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> Generator[Any, Any]:
    """
    Coroutine that collects 10 random numbers using an async
    comprehensing
    """
    return [i async for i in async_generator()]
