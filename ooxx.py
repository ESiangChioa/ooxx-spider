#!/usr/bin/env python
# coding: utf-8


import os
import sys
import re
import shutil
import requests
import datetime
from pyquery import PyQuery
from models import ImageModel

OOXX_URL = 'http://jandan.net/ooxx'
HEADERS = {
    'user-agent': 'Linux / Firefox 29: Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'
}

class Page():

    count = 0

    @classmethod
    def get_count(cls):
        """return how many pages that we have"""
        d = PyQuery(OOXX_URL, headers=HEADERS)
        cls.count = int(d('.current-comment-page:first').text().strip('[]'))

    def __init__ (self, page_number):
        """"shit"""
        self.number = page_number
        self.url = self._construct_url()

    def fetch(self):
        self.html = self._fetch_html()
        self.elements = self._get_elements()
        self.image_items = [self._gen_item(element) for element in self.elements.items()]

    def _construct_url(self):
        """ fetch page url """
        return '{}/page-{}'.format(OOXX_URL, self.number)

    def _fetch_html(self):
        return requests.get(self.url, headers=HEADERS).text

    def _get_elements(self):
        d = PyQuery(self.html)
        return d('.commentlist li').not_('.row')

    def _gen_item(self, element):
        image_item = Image()
        image_item.author = element.find('.author strong').text()
        image_url = element.find('img').attr('src')
        image_item.url = re.sub(r'cn/\w+/', r'cn/large/', image_url) # choose the larege version of image
        image_item.number = element.find('.righttext').text()
        image_item.upvote = int(element.find('.vote span').eq(1).text())
        image_item.downvote = int(element.find('.vote span').eq(2).text())
        image_item.crawl_time = datetime.datetime.now()

        return image_item


class Image():

    def __init__(self):
        self.author = ''
        self.url = ''
        self.number = 0
        self.upvote = 0
        self.downvote = 0
        self.crawl_time = None

    def save_to_db(self):
        ImageModel.create(author=self.author,
                url=self.url,
                number=self.number,
                upvote=self.upvote,
                downvote=self.downvote,
                crawl_time=self.crawl_time
                )

    def __str__(self):
        return '{},{},{},{}'.format(
            self.number, ' | ', self.upvote, self.downvote)


def crawl():
    """crawl all ooxx pages and save image urls to database"""
    Page.get_count()
    # unfortunately jandan doesn't offer page beyond 900
    for i in range(900, Page.count):
        p = Page(i)
        try:
            print('fetching ' + p.url)
            p.fetch()
        except requests.ConnectionError as e:
            print("Network Error")
        print('{} items found'.format(len(p.image_items)))
        for item in p.image_items:
            print(item)
            item.save_to_db()

def download(dir="images/"):
    for item in ImageModel.select():
        if not item.url:
            continue
        filename = dir + str(item.number) + os.path.splitext(item.url)[1]
        if os.path.exists(filename):
            print("skipping {}".format(item.number))
            continue
        print("donwloading {}".format(item.number))
        try:
            r = requests.get(item.url, stream=True, headers=HEADERS, timeout=10.0)
            with open(filename, 'wb') as f:
                r.raw.decode_content = True # force decode from gzip
                for chunk in r.iter_content(chunk_size=100*1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        except requests.ConnectionError as e:
            print("Network Error")
        except requests.exceptions.RequestException as e:
            print("Error")


if __name__ == '__main__':
    if sys.argv[1] == 'crawl':
        crawl()
    elif sys.argv[1] == 'download':
        download()
