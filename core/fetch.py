# coding: utf-8


from cookielib import CookieJar
from urllib2 import urlopen, Request, build_opener, HTTPCookieProcessor, ProxyHandler
import hashlib

from headers import make_headers
from cache import DiskCache, CacheKeyNotExistError

def build_fetch(use_cache=False, timeout=5, use_cookie=False, proxy=None, mobile=False):
    '''build fetch fucntion with proxy'''


    if use_cookie:
        cookie_handler = HTTPCookieProcessor(CookieJar())
    else:
        cookie_handler = None

    from proxy import Proxy
    if proxy and isinstance(proxy, Proxy):
        proxy_handler = ProxyHandler({'http': proxy.assemble()})
    else:
        proxy_handler = None

    handlers = [cookie_handler, proxy_handler] # more to come
    handlers = filter(lambda x: x, handlers)

    opener = build_opener(*handlers)

    if use_cache:
        cache = DiskCache()

    def fetch(url):
        if use_cache:
            key = hashlib.md5(url).hexdigest()
            try:
                return cache.get(url)
            except CacheKeyNotExistError:
                pass

        req = Request(url, headers=make_headers(mobile=mobile))
        response = opener.open(req, timeout=timeout)
        content = response.read()

        if use_cache:
            cache.set(key, content)
        return content

    return fetch 
