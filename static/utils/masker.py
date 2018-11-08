import re
from collections import deque


class Masker(object):
    def __init__(self, text):
        self.text = text
        self.alphabet = r"[a-zA-Z]"
        self.alphabetMask = self.calculateAlphabetMask()
        self.lowercaseMask = self.calculatedLowercaseMask()
        self.reducedText, self.nonAlphabetChars = self.calculateReducedText()

    def calculateAlphabetMask(self):
        alphabetList = []
        for char in list(self.text):
            if re.match(self.alphabet, char):
                alphabetList.append(1)
            else:
                alphabetList.append(0)
        return alphabetList

    def calculatedLowercaseMask(self):
        lowercaseList = []
        for char in list(self.text):
            if str.islower(char):
                lowercaseList.append(1)
            else:
                lowercaseList.append(0)
        return lowercaseList

    def calculateReducedText(self):
        result = []
        nonAlphabetChars = []
        for i, char in enumerate(list(self.text)):
            if self.alphabetMask[i] == 1:
                result.append(char.upper())
            else:
                nonAlphabetChars.append(char)
        return "".join(result), nonAlphabetChars

    def getReducedText(self):
        return self.reducedText

    def extend(self, newText):
        newText = deque(newText)
        charsToAdd = deque(self.nonAlphabetChars)
        result = []
        for i, indicator in enumerate(list(self.alphabetMask)):
            if indicator == 1:
                char = newText.popleft()
                if self.lowercaseMask[i] == 1:
                    char = char.lower()
                result.append(char)
            else:
                result.append(charsToAdd.popleft())
        return "".join(result)
