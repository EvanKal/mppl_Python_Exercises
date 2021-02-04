import os
import string
import unicodedata
import random
import codecs

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'hello.txt')
textData = []
maxWords = 1000

#Allowed characters are latin alphabet letters and space
allowedCharacters = [ord(x) for x in "".join((string.ascii_letters,chr(32),chr(39)))]

def initiate():
    f = open(my_file, "r", encoding="utf-8")
    textData = f.read().encode('ascii', 'ignore').decode('ascii', 'ignore')
    # textData = "“Who's making   personal remarks now?” the Hatter asked triumphantly.".encode('ascii', 'ignore').decode('ascii', 'ignore')
    f.close()

    print("Length before cleanUp: {}".format(len(textData)))
    textData =  cleanUpText(textData)
    print("Length after cleanUp: {}".format(len(textData)))

    textInTrios = createTrios(textData)
    finalText = generateRandomText(textInTrios)

    finalText.split(" ")
    print("Printing Final text with {} words.".format(len(finalText.split(" "))))
    print(finalText)

def cleanUpText(text):
    return ''.join([text[i] if ord(text[i]) in allowedCharacters else " " for i in range(len(text))])

def createTrios(text):
    #Normalize whitespace
    text = " ".join(text.split())

    #Split words in consecutive trios
    words = text.split(" ")
    print("Total words: {}".format(len(words)))
    allTrios = [(words[i], words[i+1], words[i+2]) for i in range(len(words)) if i+2 < len(words)]

    return allTrios

def generateRandomText(textInTrios):
    randomTextList = []
    randomTrio = random.choice(textInTrios)
    nextSentence = randomTrio

    while len(randomTextList) < maxWords-2 and len(nextSentence)>0:
        randomTextList.append(nextSentence)
        validChoicesForNextSentence = [sentence for sentence in textInTrios if sentence[0].lower() == nextSentence[1].lower() and sentence[1].lower() == nextSentence[2].lower()]
        nextSentence = random.choice(validChoicesForNextSentence if len(validChoicesForNextSentence)>0 else [()])
    
    if not nextSentence:
        print("Couldn't retrieve more than {} trios.".format(len(randomTextList)))
    else:
        print("Retrieved {} sentences.".format(len(randomTextList)))

    return " ".join(sentence[0] if randomTextList.index(sentence) < len(randomTextList)-1 else " ".join(sentence) for sentence in randomTextList)
    


initiate()