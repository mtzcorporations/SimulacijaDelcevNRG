import copy
import numpy as np
from random import random, uniform, randint
from typing import List


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def add(self,v):
        return Vector(
            v.x+self.x,
            v.y+self.y,
            v.z+self.z
        )
    def diff(self, v):
        return Vector(v.x-self.x, v.y-self.y, v.z-self.z)
    
    def normalize(self):
        d = self.length()
        if d!=0:
            return self.multiply(1/d)
        else:
            return self.multiply(1/0.001)
    
    def distance(self,v):
        dx = self.x-v.x
        dy = self.y-v.y
        dz = self.z-v.z
        return (dx**2 + dy**2 + dz**2)**0.5
    
    def length(self):
        dx = self.x
        dy = self.y
        dz = self.z
        return (dx**2 + dy**2 + dz**2)**0.5

    
    def multiply(self,s: float):
        return Vector(
            self.x * s,
            self.y * s,
            self.z * s
        )

    def copy(self):
        return Vector(self.x, self.y, self.z)
    def array(self):
        return [self.x, self.y, self.z]
    
    def __str__(self):
        return f'V({self.x},{self.y},{self.z})'

class Particle:

    def __init__(self, minMass, maxMass, minR, maxR):
        self.minMass = float(minMass)
        self.maxMass = float(maxMass)
        self.minR = float(minR)
        self.maxR = float(maxR)
        self.color = [random() for i in range(3)] + [255]

        self.loc = None
        self.v = None
        self.a = Vector()
        self.r = uniform(self.minR, self.maxR)
        self.m = uniform(self.minMass, self.maxMass)
    
    def __str__(self):
        return f'PARTICLE loc={self.loc} v={self.v} a={self.a} r={self.r} m={self.m}'

class Force:
    def __init__(self, f_type):
        self.type = f_type

    def getForce(self, p: Particle):
        raise Exception("Implmenet me!")

class Wind(Force):
    def __init__(self, strength: Vector):
        super(Wind, self).__init__('wind')
        self.strength = strength

    def getForce(self, p: Particle):
        return self.strength

class Radial(Force):
    def __init__(self, location: Vector, strength: float):

        super(Radial, self).__init__('radial')
        self.location = location
        self.strength = strength

    def getForce(self, p: Particle):
        direction = p.loc.diff(self.location).normalize()
        force = direction.multiply(self.strength)
        r = self.location.distance(p.loc)
        if r!=0:
            return force.multiply(1/r**2)
        else:
            return force.multiply(1/0.001**2)


class Gravity(Force):
    def __init__(self, strength: float):
        super(Gravity, self).__init__('gravity')
        self.strength = strength

    def getForce(self, p: Particle):
        return Vector(x=0, y=0, z=p.m * self.strength)


class Emitter:
    def __init__(self, location: Vector, minV: Vector, maxV: Vector, rate: float, max_particles: int, particles: List[Particle]):
        self.particles = particles # Tukaj imamo samo tipe particlov ki jih emitor oddaja
        self.location = location
        self.minV = minV
        self.maxV = maxV
        self.rate = rate
        self.max_particles = max_particles

    def createParticle(self):
        partType = self.particles[randint(0, len(self.particles)-1)]
        p = copy.deepcopy(partType)
        p.loc = self.location.copy()
        p.v = Vector(
            x=uniform(self.minV.x, self.maxV.x),
            y=uniform(self.minV.y, self.maxV.y),
            z=uniform(self.minV.z, self.maxV.z)
        )
        return p


class Space:
    def __init__(self, minV: Vector, maxV: Vector):
        self.minV = minV
        self.maxV = maxV
        self.t = 0

        self.types= [] # vsi type particles
        self.emitters: List[Emitter] = []
        self.particles = [] # particles ki so ustvarjeni od emittorjev
        self.forces = []

    def nextIteration(self, dt: float):
        self.t += dt

        #Ustvari particle od emittorjev
        for e in self.emitters:
            if len(self.particles) < e.max_particles:
                probability = 1/e.rate/dt 
                if random() <= probability:
                    p = e.createParticle()
                    self.particles.append(p)


        #Za vsak particle izracunaj vsoto vseh sil
        for p in self.particles:
            # Vsoto sil na delec
            forceSum = Vector()
            for f in self.forces:
                fv = f.getForce(p)
                forceSum = forceSum.add(fv)
            # Izracunaj pospešek
            p.a = forceSum.multiply(1/p.m)
            # Izracunaj novo hitrost
            p.v = p.v.add(p.a.multiply(dt))
            # Izracunaj novo lokacijo
            p.loc = p.loc.add(p.v.multiply(dt))
        

    
        

        

class SimFile:
    def __init__(self, filePath):
        self.filePath = filePath


    def import_space(self):
        space = Space(None, None)
        with open(self.filePath, 'r') as f:
            for line in f.readlines():
                line2 = line.replace('(', '').replace(')', '')
                data = line2.split(' ')[1:]
                if line.startswith('space'):
                    space.minV = Vector(*tuple(data[0:3]))
                    space.maxV = Vector(*tuple(data[3:]))
                elif line.startswith('radial'):
                    v = Vector(*tuple(data[0:3]))
                    force = Radial(location=v, strength=float(data[-1]))
                    space.forces.append(force)

                elif line.startswith('wind'):
                    v = Vector(*tuple(data[0:3]))
                    force = Wind(strength=v)
                    space.forces.append(force)

                elif line.startswith('gravity'):
                    force = Gravity(strength=float(data[-1]) if len(data) > 0 else -9.81)
                    space.forces.append(force)
                elif line.startswith('type'):
                    data = line.replace('type ', '').split(') (')
                    data = [ele.replace('(', '').replace(')', '').split() for ele in data]
                    if len(data[0]) > 1:
                        minMass, maxMass = tuple(data[0])
                    else:
                        minMass, maxMass = data[0][0], data[0][0]
                    if len(data[1]) > 1:
                        minR, maxR = tuple(data[1])
                    else:
                        minR, maxR = data[1][0], data[1][0]
                    particle = Particle(minMass, maxMass, minR, maxR)
                    space.types.append(particle)
                elif line.startswith('emitter point'):
                    data = line.replace('emitter point ', '').split(') (')
                    data = [ele.replace('(', '').replace(')', '').split() for ele in data]
                    loc = Vector(*tuple(data[0][0:3]))
                    minV = Vector(*tuple(data[1][0:3]))
                    if len(data[1]) > 3:
                        maxV = Vector(*tuple(data[1][3:]))
                    else:
                        maxV = minV
                    part = data[-2]
                    rate = data[2]
                    max_particles = data[-1]
                    particles = [space.types[int(ele)-1] for ele in part]
                    emitter = Emitter(location=loc,minV=minV, maxV=maxV, rate=float(rate[0]), max_particles=int(max_particles[0]), particles=particles)
                    space.emitters.append(emitter)
        return space
