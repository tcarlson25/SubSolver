from pycipher import SimpleSubstitution
from static.utils.substitution import SubstitutionBreak
from static.utils.transforms import Masker
from static.utils.ngram import NgramScorer
import os


class NgramSolver(object):
    def __init__(self, ciphertext, gramNum):
        self.ciphertext = ciphertext
        self.gramNum = gramNum
        directory = dir = os.path.dirname(__file__)
        ngram_files = {
            1: directory + "/en/monograms.txt",
            2: directory + "/en/bigrams.txt",
            3: directory + "/en/trigrams.txt",
            4: directory + "/en/quadgrams.txt",
        }
        self.ngramFiles = ngram_files

    def load_ngrams(self):
        ngrams = {}
        with open(self.ngramFiles[self.gramNum], "r") as f:
            for line in f:
                key, count = line.split(" ")
                ngrams[key] = int(count)
        return ngrams

    def solve(self):
        ciphertext_break, masker = Masker.from_text(self.ciphertext)
        scorer = NgramScorer(self.load_ngrams())
        breaker = SubstitutionBreak(scorer, seed=50)
        breaker.optimise(ciphertext_break, n=5)
        decryption, score, key = breaker.guess(ciphertext_break)[0]
        return key, masker.extend(decryption)
