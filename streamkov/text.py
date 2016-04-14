# -*- coding: utf-8 -*-
"""
    text
    ~~~~

    Module for cleaning, tokenizing, and yielding words from text
"""
from collections import deque


def clean(token):
    return ''.join(filter(lambda v: ord(v) < 180, token)).lower().replace('"', '')


def tokenize(line):
    return deque(map(clean, line.split()))


def decode_lines(stream):
    while 1:
        try:
            line = next(stream)
            yield line.decode('utf-8')
        except StopIteration:
            return


def generate_bigrams(line_generator):
    last_token = ''
    for line in line_generator:
        try:
            tokens = tokenize(line)
        except Exception as e:
            print(e)
            continue
        while tokens:
            current_token = tokens.popleft()
            yield (last_token, current_token)
            last_token = current_token
