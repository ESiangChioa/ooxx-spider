# coding: utf-8

from abc import ABC, abstractmethod


CACHE_DIR = './.cache'

class CacheKeyNotExistError(IndexError):
    pass


class ICache(ABC):

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass


class DiskCache(ICache):

    def __init__(self, cache_dir=CACHE_DIR):
        self.cache_dir = cache_dir

    def get(self, key):
        try:
            with open(os.path.join(self.cache_dir, key)) as fh:
                return fh.read()
        except IOError:
            raise CacheKeyNotExistError

    def set(self, key, value):
        with open(key, 'w') as fh:
            fh.write(value)
