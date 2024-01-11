#!/usr/bin/env python3
""" List of float numbers sum """
from typing import Any, Union, Sequence


# The types of the elements of the input are not know
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """ List of float numbers sum """
    if lst:
        return lst[0]
    else:
        return None
