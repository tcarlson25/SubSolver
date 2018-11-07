import re
from collections import deque


class Masker(object):
    def __init__(self, text, alphabet=r"[a-zA-Z]"):
        self.text = text
        self.alphabet = alphabet
        self.alphabet_mask = self._get_alphabet_mask()
        self.lowercase_mask = self._get_lowercase_mask()
        self.reduced_text, self.non_alphabet_chars = self._get_reduced_text()

    @staticmethod
    def from_text(text):
        masker = Masker(text)
        return masker.reduce(), masker

    def _get_alphabet_mask(self):
        return [1 if re.match(self.alphabet, char) else 0
                for char in list(self.text)]

    def _get_lowercase_mask(self):
        return [1 if str.islower(char) else 0 for char in list(self.text)]

    def _get_reduced_text(self):
        result = []
        non_alphabet_chars = []
        for i, char in enumerate(list(self.text)):
            if self.alphabet_mask[i] == 1:
                result.append(char.upper())
            else:
                non_alphabet_chars.append(char)
        return "".join(result), non_alphabet_chars

    def reduce(self):
        return self.reduced_text

    def extend(self, new_text):
        new_text = deque(new_text)
        chars_to_add = deque(self.non_alphabet_chars)
        result = []
        for i, indicator in enumerate(list(self.alphabet_mask)):
            if indicator == 1:
                char = new_text.popleft()
                if self.lowercase_mask[i] == 1:
                    char = char.lower()
                result.append(char)
            else:
                result.append(chars_to_add.popleft())
        return "".join(result)
