from static.utils.substitution import SubstitutionBreak
from static.utils.transforms import Masker
from static.utils.ngram import NgramScorer
from static.utils.wordPatterns import WordPatterns
from static.utils.simpleSubCipher import SimpleSubCipher
import os
import re, copy


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




class IntersectSolver(object):
    def __init__(self, ciphertext):
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.nonLettersOrSpacePattern = re.compile('[^A-Z\s]')
        self.ciphertext = ciphertext

    def getBlankCipherletterMapping(self):
        return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], \
        'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], \
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], \
        'X': [], 'Y': [], 'Z': []}


    def addLettersToMapping(self, letterMapping, cipherword, candidate):
        for i in range(len(cipherword)):
            if candidate[i] not in letterMapping[cipherword[i]]:
                letterMapping[cipherword[i]].append(candidate[i])



    def intersectMappings(self, mapA, mapB):
        intersectedMapping = self.getBlankCipherletterMapping()
        for letter in self.letters:
            if mapA[letter] == []:
                intersectedMapping[letter] = copy.deepcopy(mapB[letter])
            elif mapB[letter] == []:
                intersectedMapping[letter] = copy.deepcopy(mapA[letter])
            else:
                for mappedLetter in mapA[letter]:
                    if mappedLetter in mapB[letter]:
                        intersectedMapping[letter].append(mappedLetter)
        return intersectedMapping


    def removeSolvedLettersFromMapping(self, letterMapping):
        loopAgain = True
        while loopAgain:
            loopAgain = False
            solvedLetters = []
            for cipherletter in self.letters:
                if len(letterMapping[cipherletter]) == 1:
                    solvedLetters.append(letterMapping[cipherletter][0])

            for cipherletter in self.letters:
                for s in solvedLetters:
                    if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                        letterMapping[cipherletter].remove(s)
                        if len(letterMapping[cipherletter]) == 1:
                            loopAgain = True
        return letterMapping


    def getLetterMappings(self, message):
        intersectedMap = self.getBlankCipherletterMapping()
        cipherwordList = self.nonLettersOrSpacePattern.sub('', message.upper()).split()
        for cipherword in cipherwordList:
            candidateMap = self.getBlankCipherletterMapping()

            wordPattern = self.getWordPattern(cipherword)
            wordPatterns = WordPatterns()
            allPatterns = wordPatterns.getAllPatterns()
            if wordPattern not in allPatterns:
                continue

            # Add the letters of each candidate to the mapping:
            for candidate in allPatterns[wordPattern]:
                self.addLettersToMapping(candidateMap, cipherword, candidate)
            intersectedMap = self.intersectMappings(intersectedMap, candidateMap)

        return self.removeSolvedLettersFromMapping(intersectedMap)


    def getWordPattern(self, word):
        word = word.upper()
        nextNum = 0
        letterNums = {}
        wordPattern = []

        for letter in word:
            if letter not in letterNums:
                letterNums[letter] = str(nextNum)
                nextNum += 1
            wordPattern.append(letterNums[letter])
        return '.'.join(wordPattern)


    def decryptWithCipherletterMapping(self, ciphertext, letterMapping):
        key = ['x'] * len(self.letters)
        for cipherletter in self.letters:
            if len(letterMapping[cipherletter]) == 1:
                # If there's only one letter, add it to the key.
                keyIndex = self.letters.find(letterMapping[cipherletter][0])
                key[keyIndex] = cipherletter
            else:
                ciphertext = ciphertext.replace(cipherletter.lower(), '_')
                ciphertext = ciphertext.replace(cipherletter.upper(), '_')
        key = ''.join(key)
        subCipher = SimpleSubCipher()
        return subCipher.decryptMessage(key, ciphertext)

    def solve(self):
        letterMapping = self.getLetterMappings(self.ciphertext)
        foundPlaintext = self.decryptWithCipherletterMapping(self.ciphertext, letterMapping)
        return letterMapping, foundPlaintext
