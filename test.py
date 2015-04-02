import unittest
from ooxx import Page
from nose.tools import *

page = Page(1000)
page.build()

class PageTest(unittest.TestCase):

    def setUp(self):
        Page.get_count()
        self.page = page

    def test_count(self):
        assert Page.count > 1000

    def test_build_url(self):
        self.page.url = 'http://jandan.net/ooxx/page-1000' 

    def test_fetch_html(self):
        assert 'ooxx' in self.page.html 

    def test_get_elements(self):
        assert len(self.page.elements) > 0

    def test_build_item(self):
        for item in self.page.image_items:
            assert isinstance(item.author, basestring)
            assert item.number > 30000
            assert 'http' in item.url



