#!/usr/bin/env python3
"""The basics of async"""
import random
import asyncio


async def wait_random(max_delay: float = 10) -> float:
    wait = random.uniform(0.0, max_delay)
    await asyncio.sleep(wait)
    return wait
