#!/usr/bin/env python3
"""
A simple cache class that interfaces with Redis to store data
using unique keys.
"""
from typing import Union, Optional, Callable, Any
import redis
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """decorator to store the history of inputs and outputs for a particular
        function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Stores inputs and outputs of the decorated method in Redis lists.
        '''
        # Create Redis keys for input and output lists
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        # Append input arguments to the Redis list
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs_key, str(args))

        # Call the original method and store its result
        result = method(self, *args, **kwargs)

        # Append output to the Redis list
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outputs_key, str(result))

        return result
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""

    redis_client = method.__self__._redis

    # Generate Redis Keys
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    # Retrieve the history of inputs and outputs
    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    # Print the number of times the method was called
    print(f"{method.__qualname__} was called {len(inputs)} times:")

    # Iterate over the zipped inputs and outputs, and print them
    for inp, out in zip(inputs, outputs):
        print(
            f"{method.__qualname__}(*{inp.decode('utf-8')},) -> {out.decode('utf-8')}")


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

    @call_history
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
