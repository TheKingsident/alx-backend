#!/usr/bin/python3
""" 3. LRU Caching
"""

from collections import OrderedDict
from base_caching import BaseCaching
from queue import Queue


class LRUCache(BaseCaching):
    """ LRUCache class
    """
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()
        self.queue = Queue()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.queue.put(self.queue.get())
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lru_key = next(iter(self.cache_data))
                del self.cache_data[lru_key]
                print(f"DISCARD: {lru_key}")

        self.cache_data[key] = item
        self.queue.put(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
