from static.utils.masker import Masker
from static.utils.scorer import Scorer
from static.utils.wordPatterns import WordPatterns
from static.utils.subCipher import SubCipher
from pycipher import SimpleSubstitution
import os, re, copy, random


class NgramSolver(object):
    def __init__(self, ciphertext, gramNum):
        self.ciphertext = ciphertext
        self.gramNum = gramNum
        self.candidates = []
        random.seed(50)
        directory = dir = os.path.dirname(__file__)
        ngramPaths = {
            1: directory + "/en/monograms.txt",
            2: directory + "/en/bigrams.txt",
            3: directory + "/en/trigrams.txt",
            4: directory + "/en/quadgrams.txt"
        }
        self.ngramPaths = ngramPaths
        ngrams = {}
        ngramFile = open(self.ngramPaths[self.gramNum], "r")
        for line in ngramFile:
            key, value = line.split(" ")
            ngrams[key] = int(value)
        self.ngrams = ngrams

    def guess(self, text, n=3):
        result = []
        for candidate in self.candidates[0:n]:
            key, score = candidate
            decryption = SimpleSubstitution(key).decipher(text)
            result.append((decryption, score, key))
        return result

    def iterate(self, text, n):
        for i in range(n):
            key, score = self.getIteration(text)
            self.candidates.append((key, score))
            self.candidates = sorted(self.candidates, reverse=True,
                                     key=lambda t: t[1])

    # return score and the key used after one iteration
    def getIteration(self, text):
        key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        random.shuffle(key)
        score = self.scorer.score(SimpleSubstitution(key).decipher(text))
        count = 0
        while count < 1000:
            newKey = self.swap(key)
            newScore = self.scorer.score(SimpleSubstitution(newKey).decipher(text))
            if newScore > score:
                key = newKey
                score = newScore
                count = 0
            else:
                count += 1
        return key, score

    # swap 2 random characters within the key
    def swap(self, key):
        a, b = random.randint(0, 25), random.randint(0, 25)
        newKey = list(key)
        newKey[a], newKey[b] = newKey[b], newKey[a]
        return "".join(newKey)

    def solve(self):
        masker = Masker(self.ciphertext)
        ciphertext_break = masker.getReducedText()
        self.scorer = Scorer(self.ngrams)
        self.iterate(ciphertext_break, 5)
        decryption, score, key = self.guess(ciphertext_break)[0]
        return key, masker.extend(decryption)




class IntersectSolver(object):
    def __init__(self, ciphertext):
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.nonLettersOrSpacePattern = re.compile('[^A-Z\s]')
        self.ciphertext = ciphertext

    def getBlankMap(self):
        return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], \
        'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], \
        'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], \
        'X': [], 'Y': [], 'Z': []}

    def addToMapping(self, letterMapping, cipherword, candidate):
        for i in range(len(cipherword)):
            if candidate[i] not in letterMapping[cipherword[i]]:
                letterMapping[cipherword[i]].append(candidate[i])

    def getMappingIntersection(self, mapA, mapB):
        intersectedMapping = self.getBlankMap()
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
        intersectedMap = self.getBlankMap()
        cipherwordList = self.nonLettersOrSpacePattern.sub('', message.upper()).split()
        for cipherword in cipherwordList:
            candidateMap = self.getBlankMap()

            wordPattern = self.getWordPattern(cipherword)
            wordPatterns = WordPatterns()
            allPatterns = wordPatterns.getAllPatterns()
            if wordPattern not in allPatterns:
                continue

            # Add the letters of each candidate to the mapping:
            for candidate in allPatterns[wordPattern]:
                self.addToMapping(candidateMap, cipherword, candidate)
            intersectedMap = self.getMappingIntersection(intersectedMap, candidateMap)

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

    def decryptWithMapping(self, ciphertext, letterMapping):
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
        subCipher = SubCipher()
        return subCipher.decryptMessage(key, ciphertext)

    def solve(self):
        letterMapping = self.getLetterMappings(self.ciphertext)
        foundPlaintext = self.decryptWithMapping(self.ciphertext, letterMapping)
        return letterMapping, foundPlaintext
