#!/usr/bin/env python3
"""
Takes a list lst of elements of any type and returns a list of integers.
"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Return a list of integers representing the lengths of the
    elements of lst
    """
    return [(i, len(i)) for i in lst]
