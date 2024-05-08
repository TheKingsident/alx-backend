#!/usr/bin/python3
""" 4. MRU caching
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            mru_key = max(self.cache_data, key=self.cache_data.get)
            print("DISCARD: {}".format(mru_key))
            del self.cache_data[mru_key]

        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        value = self.cache_data.pop(key)
        self.cache_data[key] = value

        return value
