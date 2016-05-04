import sys
import os
import json
from xml.dom import minidom

class FileCountObject:
    def __init__(self, filePath):
        self.name = filePath
        self.totalWords = 0
        self.totalCharacters = 0

def processFiles(desiredPath):
    totalfiles = []
    totalWords = 0
    totalCharacters = 0

    for top, dirs, files in os.walk(desiredPath):
        for nm in files:
            fileStats = os.stat(os.path.join(top, nm))
            fileInfo = {
                'FileName':nm,
                'FilePath':os.path.join(top, nm)
            }
            currentFile = FileCountObject(fileInfo['FilePath'])
            # Split the extension from the path and normalise it to lowercase.
            ext = os.path.splitext(nm)[-1].lower()

            print ("File " + currentFile.name + ":")
            # Now we can simply use == to check for equality, no need for wildcards.
            if ext == ".json":
                parseJSON(currentFile)
            elif ext == ".resx":
                parseXML(currentFile, 'value')
            elif ext == ".xml":
                parseXML(currentFile, 'string')
            else:
                print( "invalid file")

            totalfiles.append(currentFile)

            print ("# of words = " + str(currentFile.totalWords))
            print ("# of characters = " + str(currentFile.totalCharacters))

    for file in totalfiles:
        totalWords += file.totalWords
        totalCharacters += file.totalCharacters

    if(totalWords > 0):
        averageLength = totalCharacters / totalWords
        print ("Average Length of the " + str(totalWords) + " words in these " + str(len(totalfiles)) + " files is: " + str(averageLength))


def parseJSON(jsonFile):
    with open(jsonFile.name) as data_file:
        jdata = json.load(data_file)

    try:
        for key, value in jdata.items():
            if isinstance(value,dict):
                for k, v in value.items():
                    #print("Key = " + k + " Value: " + v)
                    wordList = v.split(" ")
                    jsonFile.totalWords += len(wordList)
                    for word in wordList:
                        jsonFile.totalCharacters += len(word)
                        #print ("Total characters: " + str(jsonFile.totalCharacters))
            else:
                #print ("Key = " + key + " Value: " + value)
                wordList = value.split(" ")
                jsonFile.totalWords += len(wordList)
                for word in wordList:
                    jsonFile.totalCharacters += len(word)
                    #print ("Total characters: " + str(jsonFile.totalCharacters))
    except:
        print ("Error processing the json file - " + jsonFile.name)

def parseXML(resxFile, tagName):
    dom = minidom.parse(resxFile.name)
    valuesList = dom.getElementsByTagName(tagName)
    print (str(valuesList))
    for value in valuesList:
        stringVal = value.firstChild.nodeValue
        wordList = stringVal.split(" ")
        resxFile.totalWords += len(wordList)
        for word in wordList:
            resxFile.totalCharacters += len(word)

def getWordsInFiles():
    totalWords = 0
    print("Current directory: " + os.getcwd())
    for top, dirs, files in os.walk('./my_test_dir'):
        for nm in files:
            fileStats = os.stat(os.path.join(top, nm))
            fileInfo = {
                'FileName':nm,
                'FilePath':os.path.join(top, nm)
            }

            with open(fileInfo['FilePath']) as f:
                for line in f:
                    totalWords += len(line.split(" "))

path = sys.argv[1]
if os.path.exists(path):
    processFiles(path)
else:
    print("Not a valid path.")
