#!/usr/bin/env python3
""" List of float numbers sum """
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ Returns a tuple """
    return k, v ** 2
