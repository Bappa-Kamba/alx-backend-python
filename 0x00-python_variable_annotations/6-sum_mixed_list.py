#!/usr/bin/env python3
"""
Takes a list mxd_lst of integers and floats and returns their sum as a float.
"""
from typing import List, Union

def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Return the sum of a list of mixed integers and floats"""
    return sum(mxd_lst)
