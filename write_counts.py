def write(counts, fname):
	f = open(fname+'.dat', 'w')
	n = len(counts[0])
	for i in range(n):
		for j in range(n):
			f.write('{}\t{}\t{}\n'.format(i, j, counts[i][j]))