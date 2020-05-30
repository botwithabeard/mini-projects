import random

"""
Using Simulation to find out how far does the drunk reach from it's starting
point (0,0)
Using three abstractions
1) Location
2) Drunk (UsualDrunk, BiasedDrunk)
3) Field
"""

class Location(object):
    """
    docstring for Location
    """
    def __init__(self, x, y):
        """
        used as blueprint to make the Location object
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def move(self, deltaX, deltaY):
        """
        deltaX -> move on x-axis by deltaX
        deltaY -> move on x-axis by deltaY
        returns a Location object with new Location
        this function makes each location unique and hence
        this class is immutable
        """
        return Location(deltaX + self.x , deltaY + self.y)

    def distBetween(self, other):
        """
        returns the distance b/w two locations
        """
        return ((self.x - other.getX())**2 +(self.y - other.getY())**2)**0.5

    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'

class Drunk(object):
    """
    issabase class
    """
    def __init__(self,name = None):
        self.name = name

    def getName(self):
        return self.name

    def __str__(self):
        if self is not None:
            return self.name
        return 'Anonymous'

class UsualDrunk(Drunk):
    def takeStep(self):
        x, y = random.choice([ (1,0), (-1,0) , (0,1) , (0,-1) ])
        return (x,y)

class MasochistDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0.0,1.1), (0.0,-0.9),(1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)

class Field(object):
    """
    The main field where the drunk moves
    this has to be mutable because the location
    of the drunk changes
    """
    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        """
        self -> object Field
        drunk -> the drunk
        loc -> the location where the drunk has to be placed
        """
        if drunk in self.drunks:
            raise ValueError("Occupied")
        else:
            self.drunks[drunk] = loc

    def getLoc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        else:
            return self.drunks[drunk]

    def moveDrunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError("No such Drunk")
        else:
            x,y = drunk.takeStep()
            self.drunks[drunk] = self.drunks[drunk].move(x,y)

def walk(f, d, numSteps):
    start = f.getLoc(d)
    for step in range(numSteps):
        f.moveDrunk(d)
    return start.distBetween(f.getLoc(d))

def simWalks(numSteps , numTrials, dClass):
    homer = dClass()
    origin = Location(0,0)
    distances = []
    for step in range(numTrials):
        f = Field()
        f.addDrunk(homer, origin)
        distances.append(round(walk(f, homer, numSteps), 1))
    return distances

def drunkTest(walkLengths, numTrials, dClass):
    for numSteps in walkLengths:
        distances = simWalks(numSteps, numTrials,dClass)
        print(dClass.__name__, 'random walk of',numSteps, 'steps')
        print(' Mean =',round(sum(distances)/len(distances), 4))
        print(' Max =', max(distances),'Min =', min(distances))

if __name__ == '__main__':
    drunkTest((10, 100, 1000, 10000), 100, UsualDrunk)
