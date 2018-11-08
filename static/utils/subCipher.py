# Simple Substitution Cipher
# https://www.nostarch.com/crackingcodes (BSD Licensed)

import sys, random


class SubCipher(object):
    def __init__(self):
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


    def keyIsValid(self, key):
        keyList = list(key)
        lettersList = list(self.letters)
        keyList.sort()
        lettersList.sort()

        return keyList == lettersList


    def encryptMessage(self, key, message):
        return self.translateMessage(key, message, 'encrypt')


    def decryptMessage(self, key, message):
        return self.translateMessage(key, message, 'decrypt')


    def translateMessage(self, key, message, mode):
        translated = ''
        charsA = self.letters
        charsB = key
        if mode == 'decrypt':
            # For decrypting, we can use the same code as encrypting. We
            # just need to swap where the key and LETTERS strings are used.
            charsA, charsB = charsB, charsA

        # Loop through each symbol in message:
        for symbol in message:
            if symbol.upper() in charsA:
                # Encrypt/decrypt the symbol:
                symIndex = charsA.find(symbol.upper())
                if symbol.isupper():
                    translated += charsB[symIndex].upper()
                else:
                    translated += charsB[symIndex].lower()
            else:
                # Symbol is not in LETTERS; just add it
                translated += symbol

        return translated


    def getRandomKey(self):
        key = list(self.letters)
        random.shuffle(key)
        return ''.join(key)
