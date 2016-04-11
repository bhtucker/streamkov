# -*- coding: utf-8 -*-
"""
    text
    ~~~~

    Module for cleaning, tokenizing, and yielding words from text
"""

def clean(token):
    return ''.join(filter(lambda v: ord(v) < 180, token)).lower()


def tokenize(line):
    return deque(map(clean, line.split()))


def generate_tokens(line_generator):
    last_token = ''
    for line in line_generator:
        tokens = tokenize(line)
        while tokens:
            current_token = tokens.popleft()
            yield (last_token, current_token)
            last_token = current_token
