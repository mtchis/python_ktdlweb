import json
import re

from nltk.tokenize import word_tokenize

def word_tokenizeTV(_string):
    text = ""
    for x in _string:
        text = text + str(x).lower()
    text  = re.sub('[^\w\s_]', '', text)
    text = re.sub('\s+', ' ', text)
    return word_tokenize(text)


def toWords(fileIn, fileOut):
    with open(fileIn, encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
        dataOut = []
        i = 1
        for rowIn in data:
            rowOut = {
                'category' : rowIn['category'],
                'words' : word_tokenizeTV(rowIn['content'])
            }
            dataOut.append(rowOut)
            print(i)
            i = i + 1
        with open(fileOut, 'w', encoding='utf8') as outFile:
            json.dump(dataOut, outFile,  ensure_ascii=False)

def main():
    toWords("WebDataMining/example.json","out.json")
    print('Done!!!')

if __name__ == "__main__":
    main()
