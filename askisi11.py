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

#Allowed characters are latin alphabet letters and space.
allowedCharacters = [ord(x) for x in "".join((string.ascii_letters))]

#To include apostrophe toggle between previous and next line
# allowedCharacters = [ord(x) for x in "".join((string.ascii_letters,chr(39)))]

def initiate():
    f = open(my_file, "r", encoding="utf-8")
    # textData = f.read().encode('ascii', 'ignore').decode('ascii', 'ignore')
    textData = f.read()
    # textData = "“Who's making   personal remarks now?” the Hatter asked triumphantly's making   personal remarks now?” the Hatter asked triumphantly."
    # textData = "“Who's making   personal remarks now?” the Hatter asked triumphantly's making   personal remarks now?” the Hatter asked triumphantly.".encode('ascii', 'ignore').decode('ascii', 'ignore')
    f.close()

    print("Length before cleanUp: {}".format(len(textData)))
    textData =  cleanUpText(textData)
    print("Length after cleanUp: {}".format(len(textData)))

    # Split to a list of words
    textData = textData.split()

    # Group words by length in a list of sets
    wordGroups = groupWords(textData)
    printResults(wordGroups)
    

def cleanUpText(text):
    return ''.join([text[i] if ord(text[i]) in allowedCharacters else " " for i in range(len(text))])


def groupWords(textData):
    wordGroups = {}

    # Group words by length (1-19) in a dictionary of sets (key: length, value: set) to avoid duplicates
    # Sets are unordered so the order of the words is random
    for word in textData:
        wordLength = len(word)
        if wordLength<20:
            wordSet = wordGroups.get(wordLength, set())
            wordSet.add(word)
            wordGroups[wordLength] = wordSet
    

    return {k: v for k, v in sorted(wordGroups.items(), key= lambda item: item[0])} 

def printResults(wordGroups):
    # print(wordGroups)
    
    for key, value in wordGroups.items():

        wordSet1 = wordGroups.get(key)
        wordSet2 = wordGroups.get(20-key)

        pairsList = []
        if wordSet1 and wordSet2:
            print("Printing word groups for lengths {len1} and {len2}".format(len1=key, len2=20-key))

            if  wordSet1 != wordSet2:

                while len(wordSet1) > 0 and len(wordSet2) > 0:
                    pairsList.append((wordSet1.pop(), wordSet2.pop()))

            elif wordSet1 == wordSet2:
                while len(wordSet1) > 1:
                    pairsList.append((wordSet1.pop(), wordSet1.pop()))

        print("".join("Pair {index}: {word1} {word2}\n".format(index=index+1, word1=pair[0],word2=pair[1]) for index, pair in enumerate(pairsList)))
    
    #Print statistics for words left unpaired
    print("Printng statistics for the words left unpaired")
    for key, value in wordGroups.items():
        print("Count of words with length {len1}: {count}".format(len1=key, count=len(value)))


initiate()