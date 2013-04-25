import math
import random
import sys

dt = 0.01 # sec
thres = 2 #cm/sec
v = 50 #an arbitrary velocity, cm/sec
v_det = 50 #arbitary velocity inside detector; lower vel = more accuracy
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
		f.write('{0}\t{1}\t{2}\n'.format(res[0], res[1], res[2]))
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
	def __init__(self, **args):
		if 'mfp' in args:
			self.mfp = args['mfp']
			self.mass = args['mass']
		else:
			self.mass = args['mass']
			self.mfp = args['mass']/((6.022*10**23)*args['den']*args['sig']*(10**-24))

		self.descr = args['descr']

	def in_target(self, p):
		r = math.sqrt(p.pos[0]**2 + p.pos[1]**2)
		#theta = math.atan(p.pos[1]/p.pos[0])
		return (50<=p.pos[2]<=55) and 10<=r<=15

	def __str__(self):
		return self.descr

class Simulation:
	def __init__(self, target, runs, det_len, bank_size):
		'set up variables and perform runs'
		self.det_len = det_len
		self.mfp = target.mfp
		self.mass = target.mass
		self.tgt = target
		self.runs = int(runs)
		self.in_target = target.in_target
		self.d = bank_size
		self.distr = []
		for i in range(int(runs)):
			res = self.run()
			if res: self.distr.append(res)
		#out_name = self.__str__() + '.counts'
		#write(out_name, self.distr)

	def run(self):
		p = self.newpart()
		#while self.in_bounds(p) and not self.in_target(p) and not self.in_detector(p):
			#p.newpos(tuple(add(p.pos, scale(p.dir, v*dt))))
		p.newpos(tuple(add(p.pos, scale(p.dir, (55.0-p.pos[2])/p.dir[2]))))
		if self.in_target(p):
			step = scale(p.dir, -self.mfp*math.log(1-random.random()))
			p.newpos(add(p.pos, step))
		while self.in_bounds(p) and self.in_target(p):
			ndir = isodir()
			step = scale(ndir, -self.mfp*math.log(1-random.random()))
			p.newen(p.en*(1+2*dot(p.dir, ndir)/self.mass))
			p.newdir(ndir)
			p.newpos(add(p.pos, step))
		#while self.in_bounds(p) and not self.in_detector(p):
			#p.newpos(add(p.pos, scale(p.dir, v*dt)))
		p.newpos(tuple(add(p.pos, scale(p.dir, -1.0*p.pos[2]/p.dir[2]))))
		if not self.in_bounds(p): return
		#if self.in_detector(p):

		return self.detect(p)

	def in_bounds(self, p):
		return math.fabs(p.pos[0])<=(self.d/2) and math.fabs(p.pos[1])<=(self.d/2) and (-self.det_len)<=p.pos[2]<=105

	def in_detector(self, p):
		return (-self.det_len)<=p.pos[2]<=0

	def newpart(self):
		return Particle(((self.d/2)-self.d*random.random(),self.d/2-self.d*random.random(),100), (0,0,-1), 14400)

	def detect(self, p):
		while self.in_detector(p) and self.in_bounds(p):
			#if random.random() <= v*dt*R: return (p.pos[0],p.pos[1],p.en)
			#if random.random() <= -v_det*dt*p.dir[2]/det_len: return (p.pos[0],p.pos[1],p.en)
			if random.random() <= -2*v_det*dt*p.dir[2]/self.det_len: return (p.pos[0],p.pos[1],p.en)
			p.newpos(tuple(add(p.pos, scale(p.dir, v_det*dt))))
		return

	def __str__(self):
		return '{0}_runs{1}_detlen{2}_size{3}'.format(self.tgt.__str__(), self.runs, self.det_len, self.d)

def test():
	p = Particle((0.1,0.1,39), (0,0,0), 0)
	tgt = Target(1,2,3)
	ex = Experiment(tgt, 10, 8, 50)
	print ex.in_target(p)

if __name__ == "__main__":
	test()