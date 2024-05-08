#!/usr/bin/python3
""" 2. LIFO caching
"""

from queue import LifoQueue
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ FIFOCache class
    """
    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.queue = LifoQueue()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = self.queue.get()
            del self.cache_data[last_key]
            print(f"DISCARD: {last_key}")

        self.cache_data[key] = item
        self.queue.put(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
