#!/usr/bin/env python3
""" Tasks - Redis """
import redis
from typing import Union, Optional, Callable
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator for counting how many times a function has been called."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for decorator functionality."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for decorator functionality."""
        inputs = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", inputs)
        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", str(output))
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """Display the history of calls of a particular function."""
    r = redis.Redis()
    f_name = fn.__qualname__
    n_calls = r.get(f_name)

    if n_calls is not None:
        n_calls = n_calls.decode('utf-8')
    else:
        n_calls = 0

    print(f'{f_name} was called {n_calls} times:')
    inputs = r.lrange(f_name + ":inputs", 0, -1)
    outputs = r.lrange(f_name + ":outputs", 0, -1)
    for input_data, output_data in zip(inputs, outputs):
        input_str = input_data.decode('utf-8')
        output_str = output_data.decode('utf-8')
        print(f'{f_name}(*{input_str}) -> {output_str}')


class Cache:
    """Class for implementing a Cache."""

    def __init__(self):
        """Constructor Method."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis using a random key
        and return the key."""
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """Reading from Redis and recovering original type."""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Parameterizes a value from Redis to str."""
        value = self._redis.get(key)
        if value is None:
            return None
        return value.decode("utf-8")

    def get_int(self, key: str) -> Optional[int]:
        """Parameterizes a value from Redis to int."""
        value = self._redis.get(key)
        if value is None:
            return None
        try:
            return int(value.decode("utf-8"))
        except ValueError:
            return None
