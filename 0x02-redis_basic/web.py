#!/usr/bin/env python3
"""
Advanced - Module for Implementing an expiring web cache and tracker
"""

import redis
import requests
from typing import Callable
from functools import wraps


# Initialize Redis client
redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Decorator for counting requests and caching results
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that implements caching and request counting
        """
        # Increment request count for the URL
        redis_client.incr(f"count:{url}")

        # Check if the result is cached
        cached_html = redis_client.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # If not cached, call the original method
        html = method(url)

        # Cache the result with 10-second expiration
        redis_client.setex(f"cached:{url}", 10, html)

        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a URL
    """
    response = requests.get(url)
    return response.text


class WebCache:
    """
    WebCache class for advanced caching operations
    """
    def __init__(self):
        """
        Initialize WebCache
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_requests
    def get_page(self, url: str) -> str:
        """
        Get page content with caching and request tracking
        """
        return requests.get(url).text

    def get_stats(self, url: str) -> dict:
        """
        Get statistics for a specific URL
        """
        count = int(self._redis.get(f"count:{url}") or 0)
        return {"url": url, "count": count}


# Example usage
if __name__ == "__main__":
    # Using the standalone get_page function
    url = ("http://slowwly.robertomurray.co.uk/delay/1000/url/"
           "http://www.example.com")
    print(get_page(url))
    print(get_page(url))  # This should be faster due to caching

    # Using the WebCache class
    cache = WebCache()
    print(cache.get_page(url))
    print(cache.get_page(url))  # This should be faster due to caching
    print(cache.get_stats(url))  # Should show the request count
