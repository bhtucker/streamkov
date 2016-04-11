# -*- coding: utf-8 -*-
"""
    markov
    ~~~~~~

    Class for streamable markov chain
"""
from collections import Counter, defaultdict
import numpy as np


def has_sentence_boundary(bigram):
    return bigram[0].endswith('.')


class MarkovGenerator(object):
    def __init__(self):
        self.word_list = []
        self.word_index = {}
        self.word_states = defaultdict(WordState)
        self.initial_state = WordState()

    def draw(self):
        tokens = []
        word = self.initial_state.draw()
        while not word.endswith('.'):
            tokens.append(word)
            word = self.word_states[word].draw()
        tokens.append(word)
        return ' '.join(tokens).capitalize()

    def receive(self, bigram):
        if has_sentence_boundary(bigram):
            self.initial_state.receive(bigram[1])
            return
        self.word_states[bigram[0]].receive(bigram[1])


class WordState(object):
    """
    Information and methods for transitioning from a word
    """
    def __init__(self):
        self.cumsum = []
        self.labels = []
        self.count = 0.

    def receive(self, word):
        word_counts = self._recover_word_counts()
        self.count += 1

        if word not in word_counts:
            self.labels.append(word)
        word_counts[word] += 1

        self._set_cumsum(word_counts)

    def _recover_word_counts(self):
        freq_vector = [
            (self.cumsum[i] - (self.cumsum[i - 1] if i > 0 else 0.))
            for i, _ in enumerate(self.cumsum)
        ]

        return Counter({
            k: self.count * v
            for k, v in zip(self.labels, freq_vector)
        })

    def _set_cumsum(self, word_counts):
        freq_vector = [
            word_counts[w] / self.count
            for w in self.labels
        ]

        self.cumsum = []
        running_total = 0.
        for freq in freq_vector:
            running_total += freq
            self.cumsum.append(running_total)

    def draw(self):
        return self.labels[np.searchsorted(self.cumsum, np.random.rand())]
