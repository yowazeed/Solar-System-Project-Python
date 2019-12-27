import numpy as np
from scipy.spatial.distance import euclidean

from Core import gravitational_force

'''
The Body class
'''


class Body(object):
    '''
    The constructor for the class
    '''

    def __init__(self, position, velocity, mass):
        self._position = np.asanyarray(position, dtype='float64')
        self._velocity = np.asanyarray(velocity, dtype='float64')
        self.mass = mass
    '''
    Function to get a distance between the present body and the other body
    '''

    def distance(self, other):
        return euclidean(self.position, other.position)
    '''
    The gravitational force other inflicts on this Body
    other can either be a Body or an iterable of Body
    '''

    def force(self, other):
        if isinstance(other, self.__class__):
            return gravitational_force(
                self.mass, other.mass,
                self.position,  other.position,
            )
        else:
            force = np.zeros_like(self.position)
            for body in other:
                force += gravitational_force(
                    self.mass, body.mass,
                    self.position,  body.position,
                )
            return force
    '''
    The Kinetic energy for the body
    '''
    @property
    def kinetic_energy(self):
        return 0.5 * self.mass * np.linalg.norm(self.velocity)**2
    '''
    The position property
    '''
    @property
    def position(self):
        return self._position

    '''
    The position setter
    '''
    @position.setter
    def position(self, value):
        self._position = np.asanyarray(value, dtype='float64')

    '''
    The velocity property
    '''
    @property
    def velocity(self):
        return self._velocity
    '''
    The velocity setter
    '''
    @velocity.setter
    def velocity(self, value):
        self._velocity = np.asanyarray(value, dtype='float64')
