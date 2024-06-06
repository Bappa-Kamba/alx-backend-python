#!/usr/bin/env python3
"""
Takes a float n as argument and returns a function that multiplies a float by n.
"""
from typing import Callable

def make_multiplier(multiplier: float) -> Callable:
    """Return a function that multiplies a float by multiplier"""
    def multiply(n: float) -> float:
        """Return the product of n and multiplier"""
        return n * multiplier
    return multiply