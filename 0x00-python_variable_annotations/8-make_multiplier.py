#!/usr/bin/env python3
""" Returns a function """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ Returns a function """
    return lambda x: x * multiplier
