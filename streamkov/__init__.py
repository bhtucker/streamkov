# -*- coding: utf-8 -*-
"""
    streamkov
    ~~~~~~~~~

    Core module for streaming markov package
"""

CONNECTION_STRING = 'postgresql://streamkov@localhost:5432/streamkov'

import tweepy
import logging
from secrets import (
    consumer_key,
    consumer_secret,
    access_token,
    access_secret)


def get_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api

api = get_api()

LOG = 'streamkov.log'
logFormatter = logging.Formatter('%(asctime)-15s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(20)
file_handler = logging.FileHandler(LOG)
file_handler.setLevel(20)
file_handler.setFormatter(logFormatter)
logger.addHandler(file_handler)
logger.info('logging initialized')
