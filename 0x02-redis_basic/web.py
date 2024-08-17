#!/usr/bin/env python3
"""
web.py - A module for caching HTML content from URLs using Redis.

This module provides functionality to fetch and cache HTML content from
    agiven URL.
It uses a decorator to cache the result of the `get_page`
    function in Redis with
    an expiration time of 10 seconds.
Additionally, it tracks how many times a particular URL has been accessed.

Modules:
    cache_page(method: Callable) -> Callable:
        A decorator that caches the result of the `get_page` function.

    get_page(url: str) -> str:
        Fetches the HTML content of a URL and caches it with
            an expiration time.

Usage Example:
    url = "http://example.com"
    content = get_page(url)
    print(content)

Dependencies:
    - requests: For making HTTP requests.
    - redis: For interacting with Redis to cache results and
        track access counts.
"""

import redis
import requests
from typing import Callable
from functools import wraps

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)


def cache_page(method: Callable) -> Callable:
    """
    Decorator to cache the result of the get_page function.

    Args:
        method (Callable): The function to be decorated, expected
            to be `get_page`.

    Returns:
        Callable: The wrapped function with caching functionality.

    This decorator checks if the requested URL's content is already cached.
    If it is, it returns the cached content. If not, it fetches the content,
    caches it with a 10-second expiration, and tracks the number of accesses.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        cache_key = f"cache:{url}"
        count_key = f"count:{url}"

        # Check if the page is in the cache
        cached_page = r.get(cache_key)
        if cached_page:
            return cached_page.decode('utf-8')

        # Fetch the page content
        page_content = method(url)

        # Cache the result with an expiration time of 10 seconds
        r.setex(cache_key, 10, page_content)

        # Increment the access count
        r.incr(count_key)

        return page_content
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content of the given URL.

    This function makes an HTTP GET request to the provided
        URL and returns the
    HTML content as a string. The result is cached by the
        `cache_page` decorator.
    """
    response = requests.get(url)
    return response.text


# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
