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

    #Normalize whitespace
    textData = " ".join(textData.split())

    #Replace characters with mirroring character and reverse 
    textData = mirrorCharacters(textData)

    print(textData)

def cleanUpText(text):
    return ''.join([text[i] if ord(text[i]) in allowedCharacters else " " for i in range(len(text))])

def mirrorCharacters(text):
    text = [x for x in text]
    text = [getMirrorCharacter(char) for char in text]
    text.reverse()
    return ''.join(text)

def getMirrorCharacter(char):
    return chr(128-ord(char))

initiate()