import redis
from typing import Callable
import requests
from functools import wraps

r = redis.Redis(host='localhost', port='6379', db=0)


def cache_page(method: Callable) -> Callable:
    """Decorator to cache the result of get_page function."""
    @wraps(method)
    def wrapper(url: str) -> str:
        cache_key = f"cache:{url}"
        count_key = f"count:{url}"

        cached_page = r.get(cache_key)
        if cached_page:
            return cached_page.decode('utf-8')

        page_content = method(url)

        r.setex(cache_key, 10, page_content)

        r.incr(cache_key, 10, page_content)

        r.incr(count_key)

        return page_content
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
