from math import log10


class Scorer(object):
    def __init__(self, ngrams):
        self.ngrams = ngrams

        # get lengths
        lengths = {len(key) for key, value in self.ngrams.items()}
        self.n = lengths.pop()

        # get log values
        alpha = 0.01
        total = sum(value for key, value in self.ngrams.items())
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key]) / total)
        self.alpha = log10(alpha / total)

    def score(self, text):
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text) - self.n+1):
            current_token = text[i:i+self.n]
            if current_token in self.ngrams:
                score += ngrams(current_token)
            else:
                score += self.alpha
        return score
