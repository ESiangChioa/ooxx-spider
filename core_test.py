import unittest

from core.fetch import build_fetch
from core.proxy import Proxy, MimiProxyFinder, ProxyPool

class TestProxy(unittest.TestCase):

    def test_assemble(self):
        p = Proxy('http', 'localhost', '80')
        self.assertEqual(p.assemble(), 'http://localhost:80')

class TestBuildFetch(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_build_fetch_without_arguments(self):
        fetch = build_fetch()
        self.assertTrue('html' in fetch('http://www.baidu.com'))

    def test_build_fetch_with_proxy(self):
        p = Proxy('http', '113.31.46.205', '81')
        fetch = build_fetch(proxy=p)
        self.assertTrue('html' in fetch('http://www.baidu.com'))

class TestProxyFinder(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_find(self):
        finder = MimiProxyFinder()
        self.assertGreater(len(finder.find()), 0)

    def test_good_result(self):
        finder = MimiProxyFinder()
        p = finder.find()[0]
        self.assertRegexpMatches(p.protocol, r'http|https')

class TestProxyPool(unittest.TestCase):

    def test_pool(self):
        pool = ProxyPool(finder=MimiProxyFinder())
        pool.refresh()
        self.assertGreater(len(pool.pool), 0)
