#!python3

import sys

def main():
    f1 = open(sys.argv[1], 'r')
    counts1 = []
    for line in f:
        i, j, ct = (int(x) for x in line.split())
        if j == 0: counts1.append([])
        counts1[i].append(ct)

    f1.close()
    f2 = open(sys.argv[2], 'r')
    counts2 = []
    for line in f:
        i, j, ct = (int(x) for x in line.split())
        if j == 0: counts2.append([])
        counts2[i].append(ct)
    f2.close()

    diff = []
    


if __name__ == "__main__":
    main()