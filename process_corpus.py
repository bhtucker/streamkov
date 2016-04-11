import numpy as np
from collections import Counter, deque
import time


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


def assemble_counts(token_generator):
    bigram_counts = Counter()
    word_counts = Counter()
    start_words = set()

    for token_pair in token_generator:
        bigram_counts[token_pair] += 1
        word_counts[token_pair[0]] += 1
        if token_pair[0].endswith('.'):
            start_words.add(token_pair[1])
        if len(start_words) % 5 == 0:
            print len(bigram_counts)
    return bigram_counts, word_counts, start_words


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
        print 'starting math'
        self.total_start_words = float(sum([
            count
            for word, count in self.word_counts.iteritems()
            if word in self.start_words]))
        print 'starting init state'
        self.initial_state_prob_vec = np.array(
            [
                ((self.word_counts[w] if w in self.start_words else 0.0)
                 / self.total_start_words)
                for w in self.word_list]
        )

        print 'starting transition_matrix'
        self.transition_matrix = np.vstack(
            [np.array(
                [self.bigram_counts[(w1, w2)] / float(self.word_counts[w1])
                 for w2 in self.word_list]
            )
                for w1 in self.word_list
            ]
        )


def get_chain_from_file(filename):
    with open(filename, 'r') as f:
        return MarkovGenerator(*assemble_counts(generate_tokens(f)))

if __name__ == '__main__':
    mk = get_chain_from_file('on_calvinism.txt')
    print mk.draw()
