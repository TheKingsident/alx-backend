#!/usr/bin/env python3
"""1. Simple pagination """

import csv
import math
from typing import List


def index_range(page, page_size):
    """index_range that takes two integer arguments page and page_size"""
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """get_page that takes two integer arguments page and page_size"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        dataset_range = len(self.dataset())

        start_index, end_index = index_range(page, page_size)

        if start_index >= dataset_range:
            return []
        return self.dataset()[start_index:end_index]
    
    def get_hyper(self, page: int = 1, page_size: int = 10):
        dataset_range =  len(self.dataset())
        next_page = page + 1 if page * page_size < dataset_range else None
        return {
            'page_size': page_size,
            'page': page,
            'data': self.get_page(page, page_size),
            'next_page': next_page,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': math.ceil(dataset_range / page_size)       
        }
