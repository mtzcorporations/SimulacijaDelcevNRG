from typing import List


class Vector:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


class Particle:

    def __init__(self, minMass, maxMass, minR, maxR):

        self.loc = None
        self.v = None
        self.a = None
        self.minMass = float(minMass)
        self.maxMass = float(maxMass)
        self.minR = float(minR)
        self.maxR = float(maxR)

class Force:
    def __init__(self, f_type):
        self.type = f_type

    def getLocationForce(self, location: Vector):
        raise Exception("Implmenet me!")

class Wind(Force):
    def __init__(self, strength: Vector):
        super(Wind, self).__init__('wind')
        self.strength = strength

    def getLocationForce(self, location: Vector):
        raise Exception("Implmenet me!")

class Radial(Force):
    def __init__(self, location: Vector, strength: float):

        super(Radial, self).__init__('radial')
        self.location = location
        self.strenth = strength

class Gravity(Force):
    def __init__(self, strength: float):
        super(Gravity, self).__init__('gravity')
        self.strength = strength

class Emitter:
    def __init__(self, location: Vector, minV: Vector, maxV: Vector, rate: float, max_particles: int, particles: List[Particle]):
        self.particles = particles
        self.location = location
        self.minV = minV
        self.maxV = maxV
        self.rate = rate
        self.max_particles = max_particles
class Space:
    def __init__(self, minV: Vector, maxV: Vector):
        self.minV = minV
        self.maxV = maxV

        self.emitters: List[Emitter] = []
        self.particles = []
        self.forces = []

class SimFile:
    def __init__(self, filePath):
        self.filePath = filePath


    def import_simulation(self):
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
                    force = Gravity(strength=float(data[-1]) if len(data) > 0 else 9.81)
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
                    space.particles.append(particle)
                elif line.startswith('emitter point'):
                    data = line.replace('emitter point ', '').split(') (')
                    data = [ele.replace('(', '').replace(')', '').split() for ele in data]
                    loc = Vector(*tuple(data[0][0:3]))
                    minV = Vector(*tuple(data[1][0:3]))
                    if len(data[1]) > 3:
                        maxV = Vector(*tuple(data[1][3:]))
                    part = data[-2]
                    rate = data[2]
                    max_particles = data[-1]
                    particles = [space.particles[int(ele)-1] for ele in part]
                    emitter = Emitter(location=loc,minV=minV, maxV=maxV, rate=float(rate[0]), max_particles=int(max_particles[0]), particles=particles)
                    space.emitters.append(emitter)
        return space


simFile = SimFile('inputs/advanced_01.txt')
space = simFile.import_simulation()
print(space)
