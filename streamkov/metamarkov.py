# -*- coding: utf-8 -*-
"""
    metamarkov
    ~~~~~~~~~~

    Module for combining and drawing from multiple
"""
from streamkov.markov import MarkovGenerator
from functools import reduce
import random


class MetaMarkov(MarkovGenerator):
    """
    Combine multiple MarkovGenerators to draw
    """
    def __init__(self, *markov_generators):
        self.markov_generators = markov_generators
        original_lists = [c.word_list for c in markov_generators]
        words = reduce(
            lambda a, b: a.union(b),
            [set(mk.word_list) for mk in markov_generators]
        )
        self.word_list = list(words)

        self.word_index = {v: ix for ix, v in enumerate(self.word_list)}
        for child_generator in self.markov_generators:
            child_generator.index_mapper = make_mapper(child_generator, self)

        self.word_states = {
            ix: MetaWordState(self, word=v)
            for ix, v in enumerate(self.word_list)
        }

        self.initial_state = MetaWordState(self)

    def receive(self, word):
        raise NotImplementedError('The MetaMarkov is generate-only')


class MetaWordState(object):
    """
    Information and methods for transitioning from a word
    """

    def __init__(self, metamarkov, word=None):
        self.component_states = []
        for component in metamarkov.markov_generators:
            component_state = _get_component_state(component, word)
            if not component_state:
                continue
            component_state.mapper = component.index_mapper
            self.component_states.append(component_state)

    def draw(self):
        choices = reduce(
            lambda a, b: a + b,
            [c.mapped_adjacencies for c in self.component_states]
        )
        assert all([c is not None for c in choices])

        return random.choice(choices)

    def is_stop_word(self):
        return not any([c.adjacencies for c in self.component_states])


def make_mapper(child_mg, parent_mm):
    # returns a function mapping from a child's index to the master index
    return lambda v: parent_mm.word_index.get(
        child_mg.word_list[v]
    )


def _get_component_state(component, word):
    if not word:
        return component.initial_state
    component_idx = component.word_index.get(word)
    if not component_idx:
        return
    return component.word_states[component_idx]
