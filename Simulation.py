import math
import random
import sys

dt = 0.01  # sec
v_det = 50  #arbitary velocity inside detector; lower vel = more accuracy
random.seed()


class Particle:
    #def __init__(self, pos, direc, energy):
    def __init__(self, pos, direc):
        self.pos = pos
        self.dir = direc

    def newpos(self, pos):
        self.pos = pos

    def newdir(self, direc):
        self.dir = direc

'''
    def newen(self, energy):
        self.en = energy
'''

def add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))


def scale(v, a):
    return tuple(x*a for x in v)


def dot(v1, v2):
    return sum(tuple(x*y for x, y in zip(v1, v2)))


def write(fname, distr):
    with open(fname, 'w') as f:
        for i, res in enumerate(distr):
            #f.write('{0}\t{1}\t{2}\n'.format(res[0], res[1], res[2]))
            f.write('{0}\t{1}\n'.format(res[0], res[1]))


def isodir():
    r1 = random.random()
    r2 = random.random()
    w = 1 - 2*r1
    rho = math.sqrt(1 - w**2)
    phi = 2*math.pi*r2
    return (rho*math.cos(phi), rho*math.sin(phi), w)


def hemidir():
    r1 = random.random()
    r2 = random.random()
    w = r1 - 1
    rho = math.sqrt(1 - w**2)
    phi = 2*math.pi*r2
    return (rho*math.cos(phi), rho*math.sin(phi), w)


class Target:
    def __init__(self, mfp1, mfp2, r1, r2, r3, descr=None):
        self.mfp1, self.mfp2 = mfp1, mfp2
        self.r1, self.r2, self.r3 = r1, r2, r3
        if descr: self.descr = descr

    def in_target(self, p):
        r = math.sqrt(p.pos[0]**2 + p.pos[1]**2)
        return (50 <= p.pos[2] <= 55) and r <= self.r3

    def get_mfp(self, p):
        r = math.sqrt(p.pos[0]**2 + p.pos[1]**2)
        if r <= self.r1: return self.mfp1
        if r <= self.r2: return self.mfp2
        else: return self.mfp1

    def __str__(self):
        return self.descr

'''
    def get_mass(self, p):
        r = math.sqrt(p.pos[0]**2 + p.pos[1]**2)
        if r <= self.r1: return self.m1
        if r <= self.r2: return self.m2
        else: return self.m1
'''


class Simulation:
    def __init__(self, target, runs, det_len, bank_size):
        'set up variables and perform runs'
        self.det_len = det_len
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
        p.newpos(tuple(add(p.pos, scale(p.dir, (55.0-p.pos[2])/p.dir[2]))))
        if self.in_target(p):
            step = scale(p.dir, -self.tgt.get_mfp(p)*math.log(1-random.random()))
            p.newpos(add(p.pos, step))
        while self.in_bounds(p) and self.in_target(p):
            ndir = isodir()
            step = scale(ndir, -self.tgt.get_mfp(p)*math.log(1-random.random()))
            #p.newen(p.en*(1+2*dot(p.dir, ndir)/self.tgt.get_mass(p)))
            p.newdir(ndir)
            p.newpos(add(p.pos, step))
        p.newpos(tuple(add(p.pos, scale(p.dir, -1.0*p.pos[2]/p.dir[2]))))
        if not self.in_bounds(p): return

        return self.detect(p)

    def in_bounds(self, p):
        return math.fabs(p.pos[0])<=(self.d/2) and math.fabs(p.pos[1])<=(self.d/2) and (-self.det_len)<=p.pos[2]<=105

    def in_detector(self, p):
        return (-self.det_len)<=p.pos[2]<=0

    def newpart(self):
        #return Particle(((self.d/2)-self.d*random.random(),self.d/2-self.d*random.random(),100), (0,0,-1), 14400)
        return Particle(((self.d/2)-self.d*random.random(), self.d/2-self.d*random.random(), 100), (0, 0, -1))

    def detect(self, p):
        while self.in_detector(p) and self.in_bounds(p):
            #if random.random() <= -2*v_det*dt*p.dir[2]/self.det_len: return (p.pos[0],p.pos[1],p.en)
            if random.random() <= -2*v_det*dt*p.dir[2]/self.det_len: return (p.pos[0], p.pos[1])
            p.newpos(tuple(add(p.pos, scale(p.dir, v_det*dt))))
        return

    def __str__(self):
        return '{0}_runs{1}_detlen{2}_size{3}'.format(self.tgt.__str__(), self.runs, self.det_len, self.d)
