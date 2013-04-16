import math
import re
from read_counts import read_counts

def resolve(counts, n, r, x0, y0, dim, res):
	center_x = x0 + dim/2
	center_y = y0 + dim/2
	dt = 2*math.pi/res   #d_theta
	sz = 1.0*dim/n
	amp = []
	for i in range(res):
		x = r*math.cos(i*dt)
		y = r*math.sin(i*dt)
		amp.append(counts[int((x - x0)//sz)][int((y - y0)//sz)])
	avg = 1.0*sum(amp)/len(amp)
	print('avg:{}'.format(avg))
	contrast = (1.0/len(amp))*sum([(1.0*ct - avg)**2 for ct in amp])
	return contrast

if __name__ == "__main__":
	results = read_counts('L10.0_Ct20_5e5_T20kev_D50.dat')
	res = resolve(results, 20, 10, -25, -25, 50, 100)
	print(res)