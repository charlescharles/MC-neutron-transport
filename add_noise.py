import math

def add_noise(counts, k=1):
	''' return nxn array of noise-ified detector counts.
	Shifts counts towards the mean count by k standard deviations.
	'''
	noisy = []
	n = len(counts[0])
	avg_ct = sum([sum(row) for row in counts])/(n**2)
	for row in counts:
		rw = []
		for el in row:
			if el < avg_ct:
				if (avg_ct - el) < math.sqrt(el):
					rw.append(avg_ct)
				else:
					rw.append(el + math.sqrt(el))
			elif el > avg_ct:
				if (el - avg_ct) < math.sqrt(el):
					rw.append(avg_ct)
				else:
					rw.append(el - math.sqrt(el))
			else: rw.append(avg_ct)
		noisy.append(rw)

	return noisy

if __name__ == "__main__":
	print('testing add_noise.py')
	soften('soften_in.dat', 50, -100, -100, 200, 20)