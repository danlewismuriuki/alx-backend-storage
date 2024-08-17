#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

# Connect to Redis
r = redis.Redis()
'''The module-level Redis instance.
'''


def cache_data(method: Callable) -> Callable:
    '''Caches the output of fetched data and tracks access counts.
    '''
    @wraps(method)
    def wrapper(url: str) -> str:
        '''The wrapper function for caching the output and counting access.
        '''
        # Increment the access count before checking the cache
        r.incr(f'count:{url}')

        # Check if the page is in the cache
        cached_result = r.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')

        # Fetch the page content if not cached
        page_content = method(url)

        r.set(f'count:{url}', 0)
        # Cache the result with an expiration time of 10 seconds
        r.setex(f'result:{url}', 10, page_content)

        return page_content
    return wrapper


@cache_data
def get_page(url: str) -> str:
    '''Fetches the content of a URL and caches the response.
    '''
    return requests.get(url).text


# # Example usage
# if __name__ == "__main__":
#     url = "http://slowwly.robertomurray.co.uk"
#     print(get_page(url))
