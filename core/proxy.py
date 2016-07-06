# coding: utf-8

import re
import socket
import random
import httplib
from abc import ABCMeta, abstractmethod
from urllib2 import HTTPError, URLError


class Proxy:

    def __init__(self, protocol, ip, port):
        self.protocol = protocol
        self.ip = ip
        self.port = port

    def assemble(self):
        return '{}://{}:{}'.format(self.protocol, self.ip, self.port)


class IProxyFinder:

    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self):
        '''returns a list of Proxy objects'''
        pass


class MimiProxyFinder(IProxyFinder):

    def __init__(self):
        self.urls = ['http://www.mimiip.com/gngao/{}'.format(i) for i in range (5)]

    def find(self, fetch=None):
        from fetch import build_fetch

        if not fetch:
            fetch = build_fetch()
        proxies = []
        try:
            html = fetch(random.choice(self.urls))
        except IOError:
            return proxies
        rows = re.findall(r'<tr>[\s\S]*?</tr>', html)
        for row in rows:
            try:
                ip = re.search(r'\d+\.\d+\.\d+\.\d+', row).group(0)
                port = re.search(r'<td>(\d{2,4})</td>', row).group(1)
                protocol = re.search(r'<td>(HTTP|HTTPS)</td>', row).group(1).lower()
                proxies.append(Proxy(protocol, ip, port))
            except IndexError:
                pass
            except AttributeError:
                pass

        return proxies


class ProxyPool:

    def __init__(self, finder, test_url='http://www.baidu.com'):
        self.source_page = 'http://www.mimiip.com/gngao/'
        self.pool = set()
        self.test_url = 'http://www.baidu.com'
        self.finder = MimiProxyFinder()

    def refresh(self):
        self.pool = set(filter(lambda p: self._judge(p), self.pool))
        if len(self.pool) < 10:
            if len(self.pool) > 0:
                fetch = build_fetch(proxy=list(self.pool)[0])
            else:
                fetch = None
            new_proxies = filter(lambda p: self._judge(p), self.finder.find(fetch))
            for new_proxy in new_proxies:
                self.pool.add(new_proxy)

    def random_proxy(self):
        return random.choice(list(self.pool))

    def _judge(self, proxy):
        '''decide whether this proxy is alive'''
        from fetch import build_fetch
        print('judging ' + proxy.assemble())

        fetch = build_fetch(proxy=proxy, timeout=1)
        try:
            fetch(self.test_url)
        except (IOError, httplib.HTTPException):
            return False

        return True

