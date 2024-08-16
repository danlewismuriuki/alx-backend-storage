#!/usr/bin/env python3
"""
A simple cache class that interfaces with Redis to store data
using unique keys.
"""
from typing import Union, Optional, Callable
import redis
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
         A decorator that counts how many times a method is called.
        Args:
        method (Callable): The method to be wrapped by the decorator.

        Returns:
        Callable: The wrapped method with added functionality to count
        its calls in Redis.

        Example:
        @count_calls
        def some_method(self, *args):
            """
        # Create a Redis key for the method using the qualified name
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    A simple cache class that interfaces with Redis to store data
    using unique keys.

    Attributes:
    _redis : redis.Redis
        A private attribute that holds an instance of the Redis client.

    Methods:
    __init__():
        Initializes the Redis client and flushes the database.

    store(data: Union[str, bytes, int, float]) -> str:
        Generates a random key, stores the input data in Redis
        using the key,
        and returns the key.
    """

    def __init__(self):
        """
        Initialize the Cache instance.

        This method initializes the Redis client by creating
        an instance of
        `redis.Redis()` and assigns it to the private attribute `_redis`.
        It then flushes the Redis database, clearing all existing data.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Parameters:
            data : Union[str, bytes, int, float]
            The data to be stored in Redis. The data can be of
            type string,
            bytes, integer, or float.
        Returns:
        str
        The unique key under which the data has been stored
        in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable[[bytes], any]] = None
            ) -> Optional[Union[str, int, float]]:
        """
        Retrieves the value associated with the given key from Redis.
        Optionally applies a conversion function to the retrieved data.

        Args:
            key (str): The key of the data to be retrieved.
            fn (Optional[Callable[[bytes], any]]): An optional
                function to convert the data from bytes.

        Returns:
            Optional[Union[str, int, float]]: The retrieved data,
            converted if a function is provided,
            or None if the key does not exist.
        """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn:
            return fn(data)

        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves the value associated with the given key
        and converts it to a UTF-8 string.

        Args:
            key (str): The key of the data to be retrieved.

        Returns:
            Optional[str]: The retrieved value as a UTF-8 string,
            or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves the value associated with the given key
        and converts it to an integer.

        Args:
            key (str): The key of the data to be retrieved.

        Returns:
            Optional[int]: The retrieved value as an integer,
            or None if the key does not exist.
        """
        return self.get(key, fn=int)
