# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~

    Do things more reliably
"""
from functools import wraps
from streamkov import api, logger, models
import tweepy
import pickle
import math
import random
import time


def rollback_on_error(fn):
    """
    Decorator to catch sqlalchemy exceptions and rollback app's SA session
    """
    @wraps(fn)
    def wrapped(request):
        try:
            return fn(request)
        except Exception as _e:
            if getattr(_e, '__module__', None) == 'sqlalchemy.exc':
                print("Rolling back!")
                request.app['sa_session'].rollback()
            raise _e

    return wrapped


class MarkovGeneratorProxy(object):
    """
    Container for markov generator instantiated once per app
    """
    def __init__(self):
        self._mk = None

    def __getattr__(self, attr):
        if self._mk:
            return getattr(self._mk, attr)
        else:
            return getattr(self, attr)

    def set_chain(self, chain):
        self._mk = chain


def get_timeline(twitter_url, item_count=200):
    tokens = twitter_url.split('/')
    user = tokens[tokens.index('twitter.com') + 1]
    logger.info('fetching tweets for user %s' % user)
    return tweepy.Cursor(api.user_timeline, id=user).items(item_count)

# # offline mock
# def get_timeline(twitter_url):
#     with open('example_timeline.pkl', 'rb') as pkf:
#         ut = pickle.load(pkf)
#     return ut


def slow_sorted_lines(line_count=1000):
    states = models.session.query(models.Chain.state).all()
    full_word_list = [w for s in states for w in s[0]['word_list']]
    full_word_list.sort()
    for i in range(line_count):
        logger.info('slow gen: %s' % i)
        list_position = math.floor(
            (float(i) / line_count) * len(full_word_list)
        )
        current_slice = full_word_list[
            max(list_position - 50, 0): list_position + 50
        ]
        line = ' '.join(
            map(lambda i: random.choice(current_slice),  range(10))
        )
        time.sleep(.05)
        yield line
