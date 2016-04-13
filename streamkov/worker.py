# -*- coding: utf-8 -*-
"""
    worker
    ~~~~~~

    Task interface to app's MarkovGenerator
"""

from streamkov.text import generate_bigrams, decode_lines
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


@asyncio.coroutine
def dripfeeder(in_queue, out_queue):
    while True:
        item = yield from in_queue.get()
        if item.startswith('http'):
            bi_gen = bigrams_from_url(item)
        elif item.startswith('static'):
            bi_gen = bigrams_from_upload(item)
        for bigram in bi_gen:
            # print("putting %s" % str(bigram))
            yield from out_queue.put(bigram)
            asyncio.sleep(0)
