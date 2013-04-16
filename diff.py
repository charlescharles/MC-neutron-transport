#!python3

def diff(counts1, counts2):
    N = len(counts1[0])
    diff = [[0 for i in range(N)] for j in range(N)]

    for i in range(N):
        for j in range(N):
            diff[i][j] = counts1[i][j] - counts2[i][j]

    min_ct = min([min(row) for row in diff])
    diff = [[elem - min_ct for elem in row] for row in diff]

    return diff