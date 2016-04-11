# -*- coding: utf-8 -*-
"""
    markov
    ~~~~~~

    Class for streamable markov chain
"""
from collections import defaultdict
import random


class MarkovGenerator(object):
    def __init__(self):
        self.word_list = []
        self.word_index = {}
        self.word_states = defaultdict(WordState)
        self.initial_state = WordState()

    def draw(self):
        tokens = []
        word_idx = self.initial_state.draw()
        word = self.word_list[word_idx]
        while not word.endswith('.'):
            tokens.append(word)
            word_idx = self.word_states[word_idx].draw()
            word = self.word_list[word_idx]

        tokens.append(word)
        return ' '.join(tokens).capitalize()

    def receive(self, bigram):
        ix_1, ix_2 = self.bigrams_to_indices(bigram)

        if self.word_list[ix_1].endswith('.'):
            self.initial_state.receive(ix_2)
            return

        self.word_states[ix_1].receive(ix_2)

    def bigrams_to_indices(self, bigram):
        indices = []
        for word in bigram:
            if word in self.word_index:
                indices.append(self.word_index[word])
            else:
                ix = len(self.word_list)
                self.word_list.append(word)
                self.word_index[word] = ix
                indices.append(ix)
        return indices


class WordState(object):
    """
    Information and methods for transitioning from a word
    """

    def __init__(self):
        self.adjacencies = []

    def receive(self, word):
        self.adjacencies.append(word)

    def draw(self):
        return random.choice(self.adjacencies)
