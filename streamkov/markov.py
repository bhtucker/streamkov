# -*- coding: utf-8 -*-
"""
    markov
    ~~~~~~

    Class for streamable markov chain
"""
from collections import defaultdict
from cached_property import cached_property
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
                assert word == self.word_list[ix]
                self.word_index[word] = ix
                indices.append(ix)
        return indices

    def to_dict(self):
        rv = dict(initial_state=self.initial_state.adjacencies)
        rv.update({
            k: v.adjacencies for k, v in self.word_states.items()
        })
        rv.update(dict(word_list=self.word_list))
        return rv

    @classmethod
    def from_dict(cls, state):
        new = cls()
        new.word_list = state.pop('word_list')
        new.word_index = {v: ix for ix, v in enumerate(new.word_list)}
        new.initial_state = WordState(adjacencies=state.pop('initial_state'))
        for idx, adj in state.items():
            new.word_states[int(idx)] = WordState(adjacencies=adj)

        return new


class WordState(object):
    """
    Information and methods for transitioning from a word
    """

    def __init__(self, adjacencies=None):
        adjacencies = adjacencies or []
        self.adjacencies = adjacencies

    def receive(self, word):
        self.adjacencies.append(word)

    def draw(self):
        return random.choice(self.adjacencies)

    @cached_property
    def mapped_adjacencies(self):
        return list(map(self.mapper, self.adjacencies))
