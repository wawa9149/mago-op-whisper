#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN2
# AUTHORS:
# Sukbong Kwon (Galois)

import time
from typing import Callable, TypeVar

T = TypeVar('T', bound=dict[str, object])

def decoding_time_decorator(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to measure decoding time of function

    Args:
        func (function): Function to measure decoding time
    Returns:
        wrapper (function): Wrapper function to measure decoding time
    Examples:
        result = {"result": "success"}

        @measure_time
        -> result = {"result": "success", "decoding_time": 0.001}
    """
    def wrapper(*args: object, **kwargs: object) -> T:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        decoding_time = end_time - start_time
        result["decoding_time"] = round(decoding_time, 3)
        return result
    return wrapper