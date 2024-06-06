#!/usr/bin/env python3
"""
Takes a list lst of elements of any type and returns a list of integers.
"""
from typing import List, Union

def element_length(lst: List[Union[int, str]]) -> List[int]:
    """
    Return a list of integers representing the lengths of the
    elements of lst
    """
    return [len(str(x)) for x in lst]