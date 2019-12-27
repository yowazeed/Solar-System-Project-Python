import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from Body import Body
from System import SolarSystem

'''
Simulation Class is the
'''


class Simulation(object):
    '''
    The constructor 
    '''

    def __init__(self):
        data = np.genfromtxt("data.csv", delimiter=',',
                             skip_header=1, usecols=(1, 2, 3, 4, 5, 6))
        bodies = []
        self.radius = []
        for body in range(0, data[:, 0].size):
            pos = np.array([data[body][1], data[body][2]])
            mass = np.array([data[body][0]])
            velocity = np.array([data[body][3], data[body][4]])
            self.radius.append(data[body][5])
            b1 = Body(pos, velocity, mass)
            bodies.append(b1)
        '''
        Colors for the different bodies:
        Sun - Yellow
        Mercury - grey
        Venus - magenta
        Earth - blue
        Mars - red
        Satalite - white
        '''
        self.colours = ['Yellow', 'gray', 'magenta', 'blue', 'red', 'white']
        self.dt = 100000
        self.sys = SolarSystem(bodies)
        self.patches = []
        self.iter = 30000
        self.total_energy = []
        self.cross = np.zeros(len(self.sys))
        self.time = 0
        self.satalite_meeting = 0
        self.sat_cros_mars = 0
        self.period = np.zeros(len(self.sys))

    def init(self):
        return self.patches

    '''
     Running the simulation 
    '''

    def run(self):
        fig = plt.figure()
        self.ax = plt.axes()
        for i, body in enumerate(self.sys.bodies):
            self.patches.append(patches.Circle(
                (body.position), self.radius[i], animated=False, color=self.colours[i]))
        for i in range(0, len(self.patches)):
            self.ax.add_patch(self.patches[i])
        self.ax.axis('scaled')
        self.ax.set_xlim(-35e10, 35e10)
        self.ax.set_ylim(-35e10, 35e10)
        self.ax.patch.set_facecolor((0., 0., 0.))
        self.t = 0
        anim = FuncAnimation(fig, self.animate, init_func=self.init,
                             frames=self.iter, repeat=False, interval=1, blit=False)
        plt.show()

    '''
    Animating it
    '''

    def animate(self, i):
        y_list = []
        for x in range(0, len(self.sys.bodies)):
            y = (self.sys.bodies[x]. position[1])
            y_list.append(y)
        self.sys.do_beeman_integrator(self.dt)
        self.time += self.dt
        y1_list = []
        for x in range(0, len(self.sys.bodies)):
            y1 = (self.sys.bodies[x]. position[1])
            y1_list.append(y1)
        mars = self.sys.bodies[4]
        sat = self.sys.bodies[5]
        if(mars.distance(sat) < 1e10 and self.sat_cros_mars < 1):
            self.satalite_meeting = i
            self.sat_cros_mars += 1
        '''
        Checks if the any of the bodies have crossed their original y position which is 0 ans sometimes the calculator produces a number other than 0,
        therfore the program checks if the y cordinate has gone from negative to positive 
        '''
        for x in range(0, len(self.sys.bodies)):
            if(y_list[x] <= 0 and y1_list[x] >= 0 and self.cross[x] <= 1):
                self.cross[x] += 1
                self.period[x] = i
        tot = self.sys.total_energy[0]
        self.total_energy.append((self.time, tot))
        for x in range(0, len(self.patches)):
            self.patches[x].center = self.sys.bodies[x].position
        return self.patches
