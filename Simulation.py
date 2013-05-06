import math, random, sys

dt = 0.01  # sec
v_det = 50  # arbitrary velocity inside detector; lower vel = more accuracy
random.seed()


def add(v1, v2):
    """Return tuple sum of tuples by element."""
    return tuple(x + y for x, y in zip(v1, v2))


def scale(v, a):    
    """Return tuple of v scaled by a."""
    return tuple(x*a for x in v)


def dot(v1, v2):
    """Return scalar dot product of v1 and v2."""
    return sum(tuple(x*y for x, y in zip(v1, v2)))


def write(fname, distr):
    """Writes count distribution (in the form of a list of (x, y, energy)) to fname."""
    with open(fname, 'w') as f:
        for i, res in enumerate(distr):
            #f.write('{0}\t{1}\t{2}\n'.format(res[0], res[1], res[2]))
            f.write('{0}\t{1}\n'.format(res[0], res[1]))


def isodir():
    """Return a tuple of isotropically randomly generated Cartesian coords."""
    r1 = random.random()
    r2 = random.random()
    w = 1 - 2*r1
    rho = math.sqrt(1 - w**2)
    phi = 2*math.pi*r2
    return (rho*math.cos(phi), rho*math.sin(phi), w)


def hemidir():
    """Return a tuple of randomly generated Cartesian coords uniformly distributed over negative hemisphere."""
    r1 = random.random()
    r2 = random.random()
    w = r1 - 1
    rho = math.sqrt(1 - w**2)
    phi = 2*math.pi*r2
    return (rho*math.cos(phi), rho*math.sin(phi), w)


class Particle:
    """Represents a particle with energy and vector position and direction."""
    def __init__(self, pos, direc, energy):
        self.pos = pos
        self.dir = direc
        self.en = energy


class Target:
    """Represents a scattering target.
        Contains information on target geometry and composition.
    """
    def __init__(self, mfp1, mfp2, x1, dist, descr=None):
        """Initialize the target composition and geometry."""
        self.mfp1, self.mfp2 = mfp1, mfp2
        self.x1 = x1
        self.descr = descr
        self.dist = dist

    def in_target(self, p):
        """Returns true if particle is within target, false otherwise.
            Modify this to reflect target geometry
        """
        r = math.sqrt(p.pos[0]**2 + p.pos[1]**2)
        return (self.dist <= p.pos[2] <= self.dist+5) and r <= 10

    def get_mfp(self, p):
        """Return mean-free-path of target material at particle's current position."""
        r = math.sqrt(p.pos[0]**2 + p.pos[1]**2)
        rp = math.sqrt((p.pos[0] - self.x1)**2 + p.pos[1]**2)
        if rp <= 1.5: return self.mfp1
        if r <= 8: return self.mfp2
        if r <= 10: return self.mfp1

    def __str__(self):
        """Return descriptive string of this target."""
        return self.descr
'''
    def get_mass(self, p):
        r = math.sqrt(p.pos[0]**2 + p.pos[1]**2)
        if r <= self.r1: return self.m1
        if r <= self.r2: return self.m2
        else: return self.m1
'''


class Simulation:
    def __init__(self, target, runs, det_len, bank_size, dist):
        """Run a simulation, creating a list of bubbles formed.
        Keyword arguments:
        target object, number of runs, detector length, side length of detector bank
        """
        self.det_len = det_len
        self.tgt = target
        self.runs = int(runs)
        self.in_target = target.in_target
        self.d = bank_size
        self.dist = dist
        self.distr = []
        self.queue = []  # initialize queue to hold fission neutrons
        for i in range(int(runs)):
            self.run()

    def collimated_particle(self):
        """Returns a Particle at z=100 traveling in negative-z direction"""
        return Particle(((self.d/2)-self.d*random.random(), self.d/2-self.d*random.random(), self.dist + 10), (0, 0, -1), 14100)

    def run(self):
        """Simulate a single particle's path. If a bubble is formed in the detector,
            add it to the list.
        """
        if not self.queue:  # if there are no fission particles to simulate
            p = self.collimated_particle()
            p.pos = add(p.pos, scale(p.dir, ((self.dist + 5)-p.pos[2])/p.dir[2]))
        else:  # simulate fission particle if there remain any
            p = self.queue.pop()
        if self.in_target(p):
            step = scale(p.dir, -self.tgt.get_mfp(p)*math.log(1-random.random()))
            p.pos = add(p.pos, step)
        while self.in_bounds(p) and self.in_target(p):
            ndir = isodir()
            step = scale(ndir, -self.tgt.get_mfp(p)*math.log(1-random.random()))
            #p.en *= (1+2*dot(p.dir, ndir)/self.tgt.get_mass(p))
            p.dir = ndir
            p.pos = add(p.pos, step)
        p.pos = add(p.pos, scale(p.dir, -1.0*p.pos[2]/p.dir[2]))
        if self.in_bounds(p) and self.in_detector(p):
            self.detect(p)

    def in_bounds(self, p):
        """Returns true if particle is within the simulated volume; else false."""
        return math.fabs(p.pos[0]) <= (self.d/2) \
            and math.fabs(p.pos[1]) <= (self.d/2) \
            and (-self.det_len) <= p.pos[2] <= (self.dist + 20)

    def in_detector(self, p):
        """Returns true if particle is within detector bank; else false."""
        return (-self.det_len) <= p.pos[2] <= 0

    def detect(self, p):
        """Simulates particle path through detector, adding to the distribution
            if a bubble is formed.
        """
        while self.in_detector(p) and self.in_bounds(p):
            if random.random() <= -2*v_det*dt*p.dir[2]/self.det_len:
                self.distr.append((p.pos[0], p.pos[1], p.en))
            p.pos = add(p.pos, scale(p.dir, v_det*dt))

    def __str__(self):
        """Return an identifying string for this simulation containing:
            target description string, # runs, detector length, and detector bank side length
        """
        return '{0}_runs{1}_detlen{2}_size{3}'.format(self.tgt.__str__(), self.runs, self.det_len, self.d)
