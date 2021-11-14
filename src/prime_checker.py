import collections
import sys


def converter(pair):
    pair4 = []
    for el in pair:
        pair2 = el.split("', ")
        pair3 = []
        for el2 in pair2:
            pair3.append(el2.replace("'", ""))
        pair4.append(tuple(pair3))
    return pair4


inputNumber = 0
fileName = ""
if len(sys.argv) == 2:
    inputNumber = int(sys.argv[1])
    fileName = "./data/csg.txt"
elif len(sys.argv) == 3:
    inputNumber = int(sys.argv[1])
    fileName = sys.argv[2]
else:
    print("Wrong arguments count")
    exit(0)

lineList = [line.rstrip('\n') for line in open(fileName, "r")]

sigma = lineList[0].replace("sigma: {", "").replace("}", "").replace(" ", "").split(",")

lineList.pop(0)
rules = [converter(line.split(" -> ")) for line in lineList]
q = collections.deque()
tmp = set()
numOfStage1Commands = 4
q.append(["A_1"])
derivation = []


def print_stack(derivation_):
    out = open("./data/log.txt", "w")
    last_gen_index = 0
    for index, production in enumerate(derivation_):
        if any(elem in production for elem in ["A_1", "A_2"]):
            last_gen_index = index

    for index, production in enumerate(derivation_):
        if index > last_gen_index:
            out.write(str(production).lstrip('[').rstrip(']') + "\n")


while q:
    word = q.popleft()
    if tuple(word) in tmp:
        continue
    tmp.add(tuple(word))
    is_terminal = True
    for i in range(len(word)):
        if word[i] not in sigma:
            is_terminal = False
        for ix, rule in enumerate(rules):
            flag = True
            for j in range(len(rule[0])):
                if i + j >= len(word) or word[i + j] != rule[0][j]:
                    flag = False
                    break
            if flag:
                new_word = word.copy()
                for j in range(len(rule[0])):
                    new_word.pop(i)
                for j in range(len(rule[1])):
                    if rule[1][len(rule[1]) - j - 1] != "":
                        new_word.insert(i, rule[1][len(rule[1]) - j - 1])
                if any(elem in new_word for elem in ["A_1", "A_2"]):
                    q.append(new_word)
                else:
                    q.appendleft(new_word)

    derivation.append(word)
    if is_terminal:
        if inputNumber == len(word):
            print(f'{inputNumber} is a prime number')
            print_stack(derivation)
            exit(0)
        elif inputNumber < len(word):
            print(f'{inputNumber} is not a prime number')
            exit(0)
        else:
            derivation = []
