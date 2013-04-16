import math
import random
import itertools
import sys
from plot_counts import *
from write_counts import *
from add_noise import *
from resolve import *

sig = 5.45 #barns
den = 15.8 #per cm^C3
mass = 183.8 #u
thres = 2 #cm/sec
mfp = mass/((6.022*10**23)*den*sig*(10**-24))
dt = 0.01 # sec
thres = 2 #cm/sec
v = 50 #an arbitrary velocity, cm/sec
v_det = 50 #arbitary velocity inside detector; lower vel = more accuracy
d = 50 #side length of region

#det_len = 10 #cm: detector length
R = 0.1 # bubbles generated per cm traveled
random.seed()

#details of the targets
w = 20
h = 20
n = 4

class Particle:
	def __init__(self,pos,direc,energy):
		self.pos = pos
		self.dir = direc
		self.en = energy

	def newpos(self, pos):
		self.pos = pos

	def newdir(self, direc):
		self.dir = direc

	def newen(self, energy):
		self.en = energy

def add(v1,v2):
    return tuple(x + y for x, y in zip(v1, v2))

def scale(v, a):
	return tuple(x*a for x in v)

def dot(v1, v2):
	return sum(tuple(x*y for x, y in zip(v1,v2)))

'''
def in_target(p):
	if not ((50-w/2)<=p.pos[2]<=(50+w/2)): return False
	for k in range(1,n+1):
		if (-100+200*k/(n+1)-w/2) <= p.pos[1] <= (-100+200*k/(n+1)+w/2): return True
	return False
'''

'''
def in_target(p):
	#grating
	return (40<=p.pos[2]<=60) and ((-12.5 <= p.pos[1] <= 12.5) or (-12.5 <= p.pos[1]+50 <= 12.5) \
		or (-12.5 <= p.pos[1]-50 <= 12.5))
'''
'''
def in_target(p):
	#star shape
	t = math.atan(p.pos[1]/p.pos[0])
	return (40<=p.pos[2]<=60) and math.sqrt(p.pos[0]**2+p.pos[1]**2)<95 and ( (-math.pi/2<=t<=-5*math.pi/12) \
		or (-math.pi/3<=t<=-math.pi/4) or (-math.pi/6<=t<=-math.pi/12) or (0<=t<=math.pi/12) or (math.pi/6<=t<=math.pi/4) \
		or (math.pi/3<=t<=5*math.pi/12))
'''

def in_target(p, removed):
	#ring
	r = math.sqrt(p.pos[0]**2 + p.pos[1]**2)
	if removed:
		return (40<=p.pos[2]<=60) and 18<=r<=23 and not (0<=p.pos[0]<=2 and 0<=p.pos[1]<=20)
	else:
		return (40<=p.pos[2]<=60) and 18<=r<=23

def in_bounds(p, det_len):
	return math.fabs(p.pos[0])<=(d/2) and math.fabs(p.pos[1])<=(d/2) and (-det_len)<=p.pos[2]<=105

def in_detector(p, det_len):
	return (-det_len)<=p.pos[2]<=0

def isodir():
	r1 = random.random()
	r2 = random.random()
	w = 1 - 2*r1
	rho = math.sqrt(1 - w**2)
	phi = 2*math.pi*r2
	return (rho*math.cos(phi), rho*math.sin(phi),w)

def hemidir():
	r1 = random.random()
	r2 = random.random()
	w = r1 - 1
	rho = math.sqrt(1 - w**2)
	phi = 2*math.pi*r2
	return (rho*math.cos(phi), rho*math.sin(phi),w)

def newpart():
	#return Particle((100-200*random.random(),100-200*random.random(),100), hemidir(), 100)
	return Particle(((d/2)-d*random.random(),d/2-d*random.random(),100), (0,0,-1), 14400)

def detect(p, det_len):
	while in_detector(p, det_len):
		#if random.random() <= v*dt*R: return (p.pos[0],p.pos[1],p.en)
		#if random.random() <= -v_det*dt*p.dir[2]/det_len: return (p.pos[0],p.pos[1],p.en)
		if random.random() <= -2*v_det*dt*p.dir[2]/det_len: return (p.pos[0],p.pos[1],p.en)
		p.newpos(tuple(add(p.pos, scale(p.dir, v_det*dt))))
	return

def run(det_len, removed):
	p = newpart()
	while in_bounds(p, det_len) and not in_target(p, removed) and not in_detector(p, det_len):
		p.newpos(tuple(add(p.pos, scale(p.dir, v*dt))))
	if not in_bounds(p, det_len):
		return
	elif in_detector(p, det_len):
		return detect(p, det_len)
	while in_bounds(p, det_len) and in_target(p, removed):
		ndir = isodir()
		step = scale(ndir, -mfp*math.log(1-random.random()))
		#p.newen(p.en*0.95)
		#p.newen(p.en*dot(p.dir,ndir))
		p.newen(p.en*(1+2*dot(p.dir, ndir)/mass))
		p.newdir(ndir)
		p.newpos(add(p.pos, step))
		if p.en <= thres: return
	while in_bounds(p, det_len) and not in_detector(p, det_len):
		p.newpos(add(p.pos, scale(p.dir, v*dt)))
	if not in_bounds(p, det_len):
		return
	if in_detector(p, det_len):
		return detect(p, det_len)

def write_results(fname, counts):
	f = open(fname, 'w')
	for c in counts:
		f.write("%d\t%d\t%d\n" % (c[0], c[1],c[2]))

def categorize(results, n, x0, y0, dim, thres):
	''' n = number of detectors on a side; dim = side length in cm of detector bank'''
	sz = dim/n
	det = [[0 for j in range(n)] for i in range(n)]
	in_range = lambda i, j: (x0<i<(x0+dim) and y0<j<(y0+dim))
	for coord in results:
		if coord[2] >= thres and in_range(coord[0], coord[1]):
			x = int((coord[0] - x0)//sz)
			y = int((coord[1] - y0)//sz)
			det[x][y] += 1
	return det

def radial_contrast(counts, det_count, x0, y0, dim, res):
	amplitudes = []
	for i in range(40):
		amp = resolve(counts, det_count, i/4, -d/2, -d/2, d, res)
		amplitudes.append(amp)

	rad_contrast = []
	for i in range(40):
		avg = sum(amplitudes[i])/res
		contrast = math.sqrt(sum([(ct - avg)**2 for ct in amplitudes[i]])/res)
		rad_contrast.append([i/4, contrast])

	return rad_contrast

def run_comparisons():
	for k in range(10, 21):
		det_len = k/2
		runs = []

		for i in range(50000):
			res = run(det_len)
			if res:
				runs.append(res)

		for det_count in range(20, 30, 10):

			counts = categorize(runs, det_count, -d/2, -d/2, d, 20)

			rad_contrasts = radial_contrast(counts, det_count, -d/2, -d/2, d, 100)
			contrast_out = open('contrasts_L{}_Ct{}.dat'.format(det_len, det_count), 'w')
			for i in range(40):
				contrast_out.write('{}\t{}\n'.format(rad_contrasts[i][0], rad_contrasts[i][1]))

			out_name = 'L{}_Ct{}_D50'.format(det_len, det_count)
			write(counts, out_name)
			plot(counts, out_name)

			#noisy = add_noise(counts)
			#write(noisy, out_name+"_noisy")
			#plot(noisy, out_name+"_noisy")

def main():
	#for k in range(10, 21):
	#	det_len = k/2
	det_len = 8
	runs_full = []
	for i in range(50000):
		res = run(det_len, removed=False)
		if res:
			runs_full.append(res)

	runs_removed = []
	for i in range(50000):
		res = run(det_len, removed=True)
		if res:
			runs_removed.append(res)

	det_count = 25
	counts_full = categorize(runs_full, det_count, -d/2, -d/2, d, 20)
	counts_removed = categorize(runs_removed, det_count, -d/2, -d/2, d, 20)
	diff = [[0 for i in range(det_count)] for j in range(det_count)]
	for i in range(det_count):
		for j in range(det_count):
			diff[i][j] = counts_full[i][j] - counts_removed[i][j]

	out_name = 'diff_Ct{}'.format(det_count)
	write(diff, out_name)
	plot(diff, out_name)

if __name__ == "__main__":
	main()