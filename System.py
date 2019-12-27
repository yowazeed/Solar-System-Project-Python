from itertools import combinations
import scipy.constants as const


class SolarSystem:
    '''
    Constructor for the solar system 
    '''

    def __init__(self, bodies=None):
        self.bodies = bodies or []
        self.accelerations = [
            b.force(self.bodies) / b.mass
            for b in self.bodies
        ]
        self.old_acc = [
            b.force(self.bodies) / b.mass
            for b in self.bodies
        ]
    '''
    The total energy for the body
    '''
    @property
    def total_energy(self):
        return self.potential_energy + self.kinetic_energy

    '''
    The potential energy for the total energy. The formula has been updated as the 'combinations' method doesn't repeat the bodies and therefore doesn't need to be divided by 2
    '''
    @property
    def potential_energy(self):
        return -1*const.gravitational_constant * sum(
            b1.mass * b2.mass / b1.distance(b2)
            for b1, b2 in combinations(self.bodies, 2)
        )

    '''
    The Kinetic energy for the System
    '''
    @property
    def kinetic_energy(self):
        return sum(b.kinetic_energy for b in self.bodies)
    '''
    Making the len
    '''

    def __len__(self):
        return len(self.bodies)

    '''
    This method does the Beeman integration
    '''

    def do_beeman_integrator(self, delta_t):
        count = 0
        for i, (a, body) in enumerate(zip(self.accelerations, self.bodies)):
            body.position += (body.velocity * delta_t) + ((1/6)
                                                          * (4*a - self.old_acc[count])) * (delta_t*delta_t)
            count += 1
        count = 0
        for i, (a, body) in enumerate(zip(self.accelerations, self.bodies)):
            new_a = body.force(self.bodies) / body.mass
            body.velocity += ((1.0/6.0) * ((2*new_a)+(5*a) -
                                           self.old_acc[count]) * delta_t)
            self.old_acc[count] = self.accelerations[i]
            self.accelerations[i] = new_a
            count += 1
