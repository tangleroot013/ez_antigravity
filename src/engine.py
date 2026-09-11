from src.integrators import FastEuler

class GravEngine:
    def __init__(self, mass=5.972e24, G=6.674e-11, integrator=None):
        self.mass = mass
        self.G = G
        self.integrator = integrator or FastEuler()

    def get_acceleration(self, pos, vel):
        return - (self.G * self.mass) / (pos**2)

    def update(self, pos, vel, dt):
        return self.integrator.step(pos, vel, self.get_acceleration, dt)
