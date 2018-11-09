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


class FrequencySolver(object):
    def __init__(self, ciphertext):
        self.letterFrequency = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.normalDict = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
        self.nonLettersOrSpacePattern = re.compile('[^A-Z\s]')
        self.ciphertext = ciphertext
        self.cipherWords = ciphertext.split()
        self.mDict = dict()

    def Scorer(self, wordList):
        score = 0
        for word in wordList:
            if not wordnet.synsets(word):
                #Not an English Word
                score -= 1
            else:
                #English Word
                score += 1
        return score

    def GetCipherDistribution(self, cipher):
        cipher = cipher.upper()
        lettDict = dict()
        countDict = dict()

        for letter in self.letters:
            lettCount = cipher.count(letter)
            countDict[lettCount] = list()

        for letter in self.letters:
            lettCount = cipher.count(letter)
            lettDict[letter] = lettCount
            countDict[lettCount].append(letter)

        countList = sorted(countDict.keys(),reverse = True)
        returnDict = dict()
        for k in countList:
            returnDict[k] = list()
            returnDict[k].extend(countDict[k])

        return dict(sorted(lettDict.items(), key=lambda kv: kv[1], reverse=True)), returnDict

    def SolveKeys(self, str, index, wList):
        if index == len(wList):
            if(len(str) == 26):
                self.mDict[str] = 1
            return str
        else:
            permList = list(itertools.permutations(wList[index]))
            for p in permList:
                cpy_str = str
                for j in range(len(p)):
                    cpy_str += p[j]
                self.SolveKeys(cpy_str, index + 1, wList)

    def translator(self, text,alphabet,key):
        trantab = str.maketrans(alphabet,key)
        result = text.translate(trantab)
        return result

    def decrypt(self, cipherText, keys):
        plainWordList = list()
        for i in range(len(keys)):
            k = keys[i]
            pword = self.translator(cipherText, k, self.normalDict)
            plainWordList.append(pword)
        return plainWordList

    def GetScores(self, answers):
        best_score = -9999
        index = -1
        for ans in range(len(answers)):
            ansWords = answers[ans].split()
            scr = self.Scorer(ansWords)
            if scr > best_score:
                best_score = scr
                index = ans
        return best_score, index
        
    def solve(self):
        distList, countDict = self.GetCipherDistribution(self.ciphertext)
        print(distList)
        wList = list(countDict.values())
        self.SolveKeys("", 0, wList)
        keySet = set(list(self.mDict.keys()))
        print("Keys: ", len(keySet) )
        setAnswers = list(set(self.decrypt(self.ciphertext, list(self.mDict.keys()))))
        score, index = self.GetScores(setAnswers)
        return list(keySet)[index], setAnswers[index]
