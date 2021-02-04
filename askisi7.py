import os
import string
import unicodedata
import random
import codecs
import math
from collections import OrderedDict

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'hello.txt')
textData = []
maxWords = 1000

#Allowed characters are latin alphabet letters and space
allowedCharacters = [ord(x) for x in "".join((string.ascii_letters))]

def initiate():
    f = open(my_file, "r", encoding="utf-8")
    textData = f.read().encode('ascii', 'ignore').decode('ascii', 'ignore')
    # textData = "“Who's making   personal remarks now?” the Hatter asked triumphantly.".encode('ascii', 'ignore').decode('ascii', 'ignore')
    f.close()

    print("Length before cleanUp: {}".format(len(textData)))
    textData =  cleanUpText(textData)
    print("Length after cleanUp: {}".format(len(textData)))

    #Remove whitespace
    textData = "".join(textData.split())
    lettersSum = len(textData)
    lettersCount = countLetters(textData)

    printResults(lettersSum, lettersCount)

def cleanUpText(text):
    return ''.join([text[i] if ord(text[i]) in allowedCharacters else " " for i in range(len(text))])

def countLetters(text):
    counts = {}
    countsNonAscii = {}

    #Loop over the characters in text and, if it exists, increment the corresponding key's value by one, 
    #otherwise, add the character as a new key with a default value of zero incremented by one
    for letter in text:
        asciiLetter = ord(letter)
        if asciiLetter%2 != 0:
            counts[asciiLetter] = counts.get(asciiLetter, 0) + 1 
            countsNonAscii[letter] = countsNonAscii.get(letter, 0) + 1 
    
    print(counts)
    print(countsNonAscii)
    return counts

def printResults(lettersSum, lettersCount):

    lettersCount = {k: v for k, v in sorted(lettersCount.items(), key=lambda item: item[1], reverse=True)}
    for letter,count in lettersCount.items():
        percentage = count*100/lettersSum
        asterisks = "*"*math.ceil(percentage)
        printStr = "Character: {character} with ascii code {ascii} ".format(character=chr(letter), ascii=letter)
        filler = " "*(40-len(printStr))
        finalPrintStr = "".join([printStr,filler, asterisks, str(round(percentage, 2)), "%"])
        print(finalPrintStr)

initiate()