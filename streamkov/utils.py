# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~

    Do things more reliably
"""
from functools import wraps
from streamkov import api
import pickle


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


# def get_timeline(twitter_url):
#     tokens = twitter_url.split('/')
#     user = tokens[tokens.index('twitter.com') + 1]
#     return api.user_timeline(user)

# offline mock
def get_timeline(twitter_url):
    with open('example_timeline.pkl', 'rb') as pkf:
        ut = pickle.load(pkf)
    return ut
