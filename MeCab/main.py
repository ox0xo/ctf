import MeCab as mecab
import csv
from functools import reduce


mei = "名詞"
tagger= mecab.Tagger()


def morphological(test):
    result = []
    node = tagger.parseToNode(test)
    while node:
        result.append([node.surface, node.feature.split(",")[0]])
        node = node.next
    return result


def extract_noun(x, y):
    if x[1] == mei:
        if y[1] == mei:
            return [x[0] + y[0], mei]
        else:
            return [x[0] + ",", ""]
    else:
        if y[1] == mei:
            return [x[0] + y[0], mei]
        else:
            return x

def decorate(row):
    r = morphological(row[1])
    r = reduce(extract_noun, r)
    for text in r[0].split(","):
        with open("output.csv", "a", encoding="utf-8") as f:
            f.write(row[0] + ", " + text + "\n")


reader = None
with open("sample.csv", "r", encoding="utf-8") as f:
    for row in csv.reader(f):
        if len(row) > 0:
            decorate(row)