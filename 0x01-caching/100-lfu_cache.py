#!/usr/bin/python3
""" 5. LFU caching
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    """
    def __init__(self):
        """ LFUCache class
        """
        super().__init__()
        self.frequency = {}
        self.age = {}
        self.counter = 0

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.age[key] = self.counter
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lfu_keys = [k for k, v in self.frequency.items() if v == min(
                self.frequency.values())]
            lru_key = min(lfu_keys, key=lambda k: self.age[k])
            del self.cache_data[lru_key]
            del self.frequency[lru_key]
            del self.age[lru_key]
            print(f"DISCARD: {lru_key}")

        self.cache_data[key] = item
        self.frequency[key] = 1
        self.age[key] = self.counter

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        self.frequency[key] += 1
        self.age[key] = self.counter
        return self.cache_data[key]
