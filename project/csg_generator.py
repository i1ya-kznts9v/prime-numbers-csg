import argparse
import os


def csg_from_lba(path, save_path):
    line_list = [line.rstrip('\n') for line in open(path, "r")]
    init = line_list[0].split()[1]
    accept = line_list[1].split()[1]
    sigma = line_list[2].replace("sigma: {", "").replace(
        "}", "").replace(" ", "").split(",")
    gamma = line_list[3].replace("gamma: {", "").replace(
        "}", "").replace(" ", "").split(",") + sigma

    cur_line = 5
    delta = []
    while cur_line < len(line_list):
        if line_list[cur_line] == "" or line_list[cur_line][0] == "/":
            cur_line += 1
            continue
        delta.append(line_list[cur_line].replace(" ", "").split(
            ",") + line_list[cur_line + 1].replace(" ", "").split(","))
        cur_line += 3

    rules = []
    # 1+4
    for a in sigma:
        rules.append((["A_1"], ["[" + init + ", #, " + a + ", " + a + ", #]"]))
        rules.append((["A_1"], ["[" + init + ", #, " + a + ", " + a + "]", "A_2"]))
        rules.append((["A_2"], ["[" + a + ", " + a + "]", "A_2"]))
        rules.append((["A_2"], ["[" + a + ", " + a + ", #]"]))
    # 2
    for de in delta:
        for a in sigma:
            if de[4] == ">":
                if de[1] == "#":
                    for e in gamma:
                        rules.append((["[" + de[0] + ", #, " + e + ", " + a + ", #]"],  # 2.1
                                      ["[#, " + de[2] + ", " + e + ", " + a + ", #]"]))
                else:
                    rules.append((["[#, " + de[0] + ", " + de[1] + ", " + a + ", #]"],  # 2.3
                                  ["[#, " + de[3] + ", " + a + ", " + de[2] + ", #]"]))
            else:
                if de[1] == "#":
                    for e in gamma:
                        rules.append((["[#, " + e + ", " + a + ", " + de[0] + ", #]"],  # 2.4
                                      ["[#, " + de[2] + ", " + e + ", " + a + ", #]"]))
                else:
                    rules.append((["[#, " + de[0] + ", " + de[1] + ", " + a + ", #]"],  # 2.2
                                  ["[" + de[2] + ", #, " + de[3] + ", " + a + ", #]"]))
    # 3
    for a in sigma:
        for x in gamma:
            rules.append((["[" + accept + ", #, " + x + ", " + a + ", #]"],
                          [a]))
            rules.append((["[#, " + accept + ", " + x + ", " + a + ", #]"],
                          [a]))
            rules.append((["[#, " + x + ", " + a + ", " + accept + ", #]"],
                          [a]))

    # 5
    for de in delta:
        for a in sigma:
            if de[4] == ">":
                if de[1] == "#":
                    for e in gamma:
                        rules.append((["[" + de[0] + ", #, " + e + ", " + a + "]"],
                                      ["[#, " + de[2] + ", " + e + ", " + a + "]"]))
                else:
                    for z in gamma:
                        for b in sigma:
                            rules.append((["[#, " + de[0] + ", " + de[1] + ", " + a + "]", "[" + z + ", " + b + "]"],
                                          ["[#, " + de[3] + ", " + a + "]", "[" + de[2] + ", " + z + ", " + b + "]"]))
                            rules.append(
                                (["[#, " + de[0] + ", " + de[1] + ", " + a + "]", "[" + z + ", " + b + ", #]"],
                                 ["[#, " + de[3] + ", " + a + "]", "[" + de[2] + ", " + z + ", " + b + ", #]"]))
            else:
                rules.append((["[#, " + de[0] + ", " + de[1] + ", " + a + "]"],
                              ["[" + de[2] + ", #, " + de[3] + ", " + a + "]"]))
    # 6
    for de in delta:
        for a in sigma:
            for b in sigma:
                if de[4] == ">":
                    for z in gamma:
                        rules.append((["[" + de[0] + ", " + de[1] + ", " + a + "]", "[" + z + ", " + b + "]"],
                                      ["[" + de[3] + ", " + a + "]", "[" + de[2] + ", " + z + ", " + b + "]"]))
                        rules.append((["[" + de[0] + ", " + de[1] + ", " + a + "]", "[" + z + ", " + b + ", #]"],
                                      ["[" + de[3] + ", " + a + "]", "[" + de[2] + ", " + z + ", " + b + ", #]"]))
                else:
                    for z in gamma:
                        rules.append((["[" + z + ", " + b + "]", "[" + de[0] + ", " + de[1] + ", " + a + "]"],
                                      ["[" + de[2] + ", " + z + ", " + b + "]", "[" + de[3] + ", " + a + "]"]))
                        rules.append((["[#, " + z + ", " + b + "]", "[" + de[0] + ", " + de[1] + ", " + a + "]"],
                                      ["[#, " + de[2] + ", " + z + ", " + b + "]", "[" + de[3] + ", " + a + "]"]))
    # 7
    for de in delta:
        for a in sigma:
            if de[4] == ">":
                rules.append((["[" + de[0] + ", " + de[1] + ", " + a + ", #]"],
                              ["[" + de[3] + ", " + a + ", " + de[2] + ", #]"]))
            else:
                if de[1] == "#":
                    for e in gamma:
                        rules.append((["[" + e + ", " + a + ", " + de[0] + ", #]"],
                                      ["[" + de[2] + ", " + e + ", " + a + ", #]"]))
                else:
                    for z in gamma:
                        for b in sigma:
                            rules.append((["[" + z + ", " + b + "]", "[" + de[0] + ", " + de[1] + ", " + a + ", #]"],
                                          ["[" + de[2] + ", " + z + ", " + b + "]", "[" + de[3] + ", " + a + ", #]"]))
    # 8
    for a in sigma:
        for x in gamma:
            rules.append((["[" + accept + ", #, " + x + ", " + a + "]"],
                          [a]))
            rules.append((["[#, " + accept + ", " + x + ", " + a + "]"],
                          [a]))
            rules.append((["[" + accept + ", " + x + ", " + a + "]"],
                          [a]))
            rules.append((["[" + accept + ", " + x + ", " + a + ", #]"],
                          [a]))
            rules.append((["[" + x + ", " + a + ", " + accept + ", #]"],
                          [a]))
    # 9
    for a in sigma:
        for b in sigma:
            for x in gamma:
                rules.append(([a, "[" + x + ", " + b + "]"],
                              [a, b]))
                rules.append(([a, "[" + x + ", " + b + ", #]"],
                              [a, b]))
                rules.append((["[" + x + ", " + a + "]", b],
                              [a, b]))
                rules.append((["[#, " + x + ", " + a + "]", b],
                              [a, b]))

    tmp_file = "./data/tmp_csg.txt"
    tmp = open(tmp_file, "w")

    tmp.write(line_list[2] + "\n")  # sigma
    for a, b in rules:
        if "" in a:
            a.remove("")
        if "" in b:
            b.remove("")
        s1 = str(a)[1:-1] + " -> " + str(b)[1:-1]
        tmp.write(s1 + "\n")
    tmp.close()

    def converter(pair):
        pair4 = []
        for el in pair:
            pair2 = el.split("', ")
            pair3 = []
            for el2 in pair2:
                pair3.append(el2.replace("'", ""))
            pair4.append(tuple(pair3))
        return pair4

    line_list = [line.rstrip('\n') for line in open(tmp_file, "r")]

    # sigma = line_list[0].replace("sigma: {", "").replace(
    #     "}", "").replace(" ", "").split(",")

    line_list.pop(0)
    rules = [converter(line.split(" -> ")) for line in line_list]

    size = 7
    num_of_stage1_commands = 4
    active_rules = set()
    q = []
    stage2 = []
    tmp = set()
    q.append(["A_1"])
    while q:
        word = q.pop(0)
        if tuple(word) in tmp:
            continue
        tmp.add(tuple(word))
        is_terminal = True
        for i in range(len(word)):
            if word[i] in ["A_1", "A_2", "A_3", "A_4"]:
                is_terminal = False
            for ix, rule in enumerate(rules[:num_of_stage1_commands]):
                flag = True
                for j in range(len(rule[0])):
                    if i + j >= len(word) or word[i + j] != rule[0][j]:
                        flag = False
                        break
                if flag:
                    active_rules.add(ix)
                    new_word = word.copy()
                    for j in range(len(rule[0])):
                        new_word.pop(i)
                    for j in range(len(rule[1])):
                        if rule[1][len(rule[1]) - j - 1] != "":
                            new_word.insert(i, rule[1][len(rule[1]) - j - 1])
                    if len(new_word) <= size:
                        q.append(new_word)

        if is_terminal:
            stage2.append(word)
    # for i in stage2:
    #     print(i)
    st = set()
    while stage2:
        word = stage2.pop(0)
        if tuple(word) in st:
            continue
        st.add(tuple(word))
        # is_terminal = True
        for i in range(len(word)):
            # if word[i] not in sigma:
            #     is_terminal = False
            for ix, rule in enumerate(rules[num_of_stage1_commands:]):
                flag = True
                for j in range(len(rule[0])):
                    if i + j >= len(word) or word[i + j] != rule[0][j]:
                        flag = False
                        break
                if flag:
                    active_rules.add(ix + num_of_stage1_commands)
                    new_word = word.copy()
                    for j in range(len(rule[0])):
                        new_word.pop(i)
                    for j in range(len(rule[1])):
                        if rule[1][len(rule[1]) - j - 1] != "":
                            new_word.insert(i, rule[1][len(rule[1]) - j - 1])
                    stage2.append(new_word)
                    # print(new_word)
        # if is_terminal:
        #     for i in word:
        #         print(i, end = "")
        #     print()
    out = open(save_path, "w")
    line_list = [line.rstrip('\n') for line in open(tmp_file, "r")]
    out.write(line_list[0] + "\n")
    for ix, rule in enumerate(line_list):
        if ix - 1 in active_rules:
            out.write(rule + "\n")

    out.close()
    os.remove(tmp_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-lba", "--lba_path", help="Path to lba file", required=False, type=str,
                        default="./data/lba.txt")
    parser.add_argument("-g", "--grammar_path", help="Output grammar path", required=False,
                        type=str, default="./data/csg.txt")
    args = parser.parse_args()

    csg_from_lba(args.lba_path, args.grammar_path)


if __name__ == '__main__':
    main()
