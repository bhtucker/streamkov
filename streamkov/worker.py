# -*- coding: utf-8 -*-
"""
    worker
    ~~~~~~

    Task interface to app's MarkovGenerator
"""

from streamkov.text import generate_bigrams, decode_lines
from streamkov.utils import get_timeline
import requests
import asyncio


@asyncio.coroutine
def receiver(queue, mk):
    while True:
        item = yield from queue.get()
        # print("receiving %s" % str(item))
        mk.receive(item)
        asyncio.sleep(0)


def bigrams_from_url(url):
    r = requests.get(url, stream=True)
    return generate_bigrams(decode_lines(r.iter_lines()))


def bigrams_from_upload(filename):
    with open(filename, 'r') as f:
        yield from generate_bigrams(f)


def bigrams_from_twitter(twitter_url):
    # eg 'twitter.com/realDonaldTrump'
    return generate_bigrams((v.text for v in get_timeline(twitter_url)))


@asyncio.coroutine
def dripfeeder(in_queue, out_queue):
    while True:
        item = yield from in_queue.get()
        if 'twitter.com' in item:
            bi_gen = bigrams_from_twitter(item)
        elif item.startswith('http'):
            bi_gen = bigrams_from_url(item)
        elif item.startswith('static'):
            bi_gen = bigrams_from_upload(item)
        for bigram in bi_gen:
            # print("putting %s" % str(bigram))
            yield from out_queue.put(bigram)
            asyncio.sleep(0)
