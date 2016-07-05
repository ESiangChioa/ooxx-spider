# coding: utf-8


from cookielib import CookieJar
from urllib2 import urlopen, Request, build_opener, HTTPCookieProcessor, ProxyHandler

from headers import make_headers

def build_fetch(timeout=5, use_cookie=False, proxy=None, mobile=False):
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

    def fetch(url):
        req = Request(url, headers=make_headers(mobile=mobile))
        response = opener.open(req, timeout=timeout)
        return response.read()

    return fetch 
