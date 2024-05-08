#!/usr/bin/python3
""" 1. FIFO caching
"""

from queue import Queue
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class
    """
    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.queue = Queue()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            oldest_key = self.queue.get()
            del self.cache_data[oldest_key]
            print(f"DISCARD: {oldest_key}")

        self.cache_data[key] = item
        self.queue.put(key)

    def get(self, key):
        """ Get an item by key
        """
        if key in self.cache_data:
            return self.cache_data[key]
        return None
