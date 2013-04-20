import math
import random
import sys

dt = 0.01 # sec
thres = 2 #cm/sec
v = 50 #an arbitrary velocity, cm/sec
v_det = 50 #arbitary velocity inside detector; lower vel = more accuracy
d = 40 #side length of region

#det_len = 10 #cm: detector length
R = 0.1 # bubbles generated per cm traveled
random.seed()

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

def write(fname, distr):
	f = open(fname, 'w')
	for res in distr:
		f.write('{}\n'.format(res))
	f.close()


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


class Target:
	def __init__(self, sig, den, mass):
		sig = 5.45 #barns
		den = 15.8 #per cm^C3
		#den = 14.2 #reduced by 10%
		#den = 7.9 #reduced by 50%
		#den = 12.64 #reduced by 20%
		mass = 183.8 #u
		self.mass = mass
		self.mfp = mass/((6.022*10**23)*den*sig*(10**-24))

	def in_target(self, p):
		#ring
		r = math.sqrt(p.pos[0]**2 + p.pos[1]**2)
		theta = math.atan(p.pos[1]/p.pos[0])

		#local 10% diversion
		#return (47.5<=p.pos[2]<=52.5) and 10<=r<=15 and not (0<=theta<=math.pi/5 and p.pos[0] > 0)

		#spread-out 10% diversion
		#return (47.5<=p.pos[2]<=52.5) and 10<=r<=14.577

		#thickness 10% reduction
		#return (47.75<=p.pos[2]<=52.25) and 10<=r<=15

	def __str__(self):
		return 'tungsten_ring'

class Experiment:
	def __init__(self, target, runs, det_len, bank_size):
		'set up variables and perform runs'
		self.det_len = det_len
		self.mfp = target.mfp
		self.mass = target.mass
		self.in_target = target.in_target
		self.d = bank_size
		distr = []
		for i in range(runs):
			res = self.run()
			if res: distr.append(res)
		out_name = '{0}_runs{1}_detlen{2}_size{3}.counts'.format(target.__str__(), runs, det_len, bank_size)
		write(out_name,distr)

	def run(self):
		p = self.newpart()
		while self.in_bounds(p) and not self.in_target(p) and not self.in_detector(p):
			p.newpos(tuple(add(p.pos, scale(p.dir, v*dt))))
		if self.in_target(p):
			step = scale(p.dir, -self.mfp*math.log(1-random.random()))
			p.newpos(add(p.pos, step))
		while self.in_bounds(p) and self.in_target(p):
			ndir = isodir()
			step = scale(ndir, -self.mfp*math.log(1-random.random()))
			p.newen(p.en*(1+2*dot(p.dir, ndir)/self.mass))
			p.newdir(ndir)
			p.newpos(add(p.pos, step))
		while self.in_bounds(p) and not self.in_detector(p):
			p.newpos(add(p.pos, scale(p.dir, v*dt)))
		if not self.in_bounds(p):
			return
		if self.in_detector(p):
			return self.detect(p)

	def in_bounds(self, p):
		return math.fabs(p.pos[0])<=(self.d/2) and math.fabs(p.pos[1])<=(self.d/2) and (-self.det_len)<=p.pos[2]<=105

	def in_detector(self, p):
		return (-self.det_len)<=p.pos[2]<=0

	def newpart(self):
		return Particle(((self.d/2)-d*random.random(),self.d/2-self.d*random.random(),100), (0,0,-1), 14400)

	def detect(self, p):
		while self.in_detector(p):
			#if random.random() <= v*dt*R: return (p.pos[0],p.pos[1],p.en)
			#if random.random() <= -v_det*dt*p.dir[2]/det_len: return (p.pos[0],p.pos[1],p.en)
			if random.random() <= -2*v_det*dt*p.dir[2]/self.det_len: return (p.pos[0],p.pos[1],p.en)
			p.newpos(tuple(add(p.pos, scale(p.dir, v_det*dt))))
		return

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

def main():
	tgt = Target(1,2,3)
	ex = Experiment(tgt, 10, 8, 50)

def test():
	p = Particle((0.1,0.1,39), (0,0,0), 0)
	tgt = Target(1,2,3)
	ex = Experiment(tgt, 10, 8, 50)
	print ex.in_target(p)

if __name__ == "__main__":
	test()