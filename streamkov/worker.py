# -*- coding: utf-8 -*-
"""
    worker
    ~~~~~~

    Task interface to app's MarkovGenerator
"""

from streamkov.text import generate_bigrams, decode_lines
from streamkov.utils import get_timeline, slow_sorted_lines
from streamkov import logger
import requests
import asyncio


@asyncio.coroutine
def receiver(queue, mk):
    while True:
        item = yield from queue.get()
        logger.info("receiving %s" % str(item))
        mk.receive(item)
        yield from asyncio.sleep(0)


def bigrams_from_url(url):
    r = requests.get(url, stream=True)
    return generate_bigrams(decode_lines(r.iter_lines()))


def bigrams_from_upload(filename):
    with open(filename, 'r') as f:
        yield from generate_bigrams(f)


def bigrams_from_twitter(twitter_url):
    # eg 'twitter.com/realDonaldTrump'
    return generate_bigrams((v.text for v in get_timeline(twitter_url)))


def demonstration_bigrams():
    return generate_bigrams(slow_sorted_lines())


@asyncio.coroutine
def dripfeeder(file_queue, bigram_queue):
    while True:
        item = yield from file_queue.get()
        logger.info('handling %s' % item)
        if 'twitter.com' in item:
            logger.info('handling %s as twitter' % item)
            bi_gen = bigrams_from_twitter(item)
        elif 'demo' in item:
            logger.info('handling %s as demo!!' % item)
            bi_gen = demonstration_bigrams()
        elif item.startswith('http'):
            logger.info('handling %s as text url' % item)
            bi_gen = bigrams_from_url(item)
        elif item.startswith('static'):
            logger.info('handling %s as local file' % item)
            bi_gen = bigrams_from_upload(item)
        for bigram in bi_gen:
            logger.info("putting %s" % str(bigram))
            yield from bigram_queue.put(bigram)
            yield from asyncio.sleep(0)
