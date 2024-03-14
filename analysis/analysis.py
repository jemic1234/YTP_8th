from analysis.D import senti as sentiD
from analysis.F import senti as sentiF
from analysis.T import senti as sentiT

def split_string(input_str):
    split_list = []

    for i in range(0, len(input_str), 512):
        split_list.append(input_str[i:i+512])
    
    return split_list

def check(text: str, cmd):
    lt = split_string(text)
    w = [0, 0, 0]
    for i in lt:
        if cmd == 'D':
            tmp = sentiD(i)
        elif cmd == 'F':
            tmp = sentiF(i)
        else:
            tmp = sentiT(i)

        for j in range(3):
            w[j] += tmp[j] * len(i)
    sum = w[0] + w[1] + w[2]
    for i in range(3):
        w[i] /= sum
    
    if w[1] > 0.4:
        return 1
    if w[0] > w[1] and w[0] > w[2]:
        return 0
    elif w[1] > w[0] and w[1] > w[2]:
        return 1
    else:
        return 2