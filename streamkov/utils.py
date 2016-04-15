# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~

    Do things more reliably
"""
from functools import wraps


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
