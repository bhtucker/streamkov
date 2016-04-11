# -*- coding: utf-8 -*-
"""
    markov
    ~~~~~~
 
    Class for streamable markov chain
"""
from collections import Counter, defaultdict
import numpy as np


class MarkovGenerator(object):
    def __init__(self, bigram_counts, word_counts, start_words):
        self.bigram_counts = bigram_counts
        self.word_counts = word_counts
        self.word_list = word_counts.keys()
        self.start_words = start_words
        self._do_math()

    def draw(self):
        tokens = []
        word_idx = int(np.random.multinomial(
            1, self.initial_state_prob_vec
        ).argmax())
        word = self.word_list[word_idx]
        while not word.endswith('.'):
            tokens.append(word)
            word_idx = int(np.random.multinomial(
                1, self.transition_matrix[word_idx, :]
            ).argmax())
            word = self.word_list[word_idx]
        tokens.append(word)
        return ' '.join(tokens).capitalize()

    def _do_math(self):
        self.total_start_words = float(sum([
            count
            for word, count in self.word_counts.iteritems()
            if word in self.start_words]))
        self.initial_state_prob_vec = np.array(
            [
                ((self.word_counts[w] if w in self.start_words else 0.0)
                 / self.total_start_words)
                for w in self.word_list]
        )
        self.transition_matrix = np.vstack(
            [np.array(
                [self.bigram_counts[(w1, w2)] / float(self.word_counts[w1])
                 for w2 in self.word_list]
            )
                for w1 in self.word_list
            ]
        )
