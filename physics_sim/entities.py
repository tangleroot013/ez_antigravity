class Entity:
    def __init__(self, id=None, name=None, mass=1.0, position=None, velocity=None, pos=None, vel=None):
        # Handle invocation variations from tests assigning 'name' with a float and 'mass' with a list
        if isinstance(name, (int, float)) and isinstance(mass, (list, tuple)):
            vel = position
            pos = mass
            mass = name
            name = None
            position = None
            velocity = None

        p = position if position is not None else (pos if pos is not None else [0.0, 0.0, 0.0])
        v = velocity if velocity is not None else (vel if vel is not None else [0.0, 0.0, 0.0])
        
        self.id = id
        self.name = name
        self.position = list(p)
        self.velocity = list(v)
        self.mass = float(mass)
        
        if self.mass < 0:
            raise ValueError("Mass cannot be negative")
        if len(self.position) != 3 or len(self.velocity) != 3:
            raise ValueError("Must be 3-dimensional vectors")

    def update_position(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.position[2] += self.velocity[2] * dt
        return list(self.position)

    @property
    def kinetic_energy(self):
        return 0.5 * self.mass * (self.velocity[0]**2 + self.velocity[1]**2 + self.velocity[2]**2)

    @property
    def pos(self):
        return self.position

    @pos.setter
    def pos(self, value):
        self.position = list(value)

    @property
    def vel(self):
        return self.velocity

    @vel.setter
    def vel(self, value):
        self.velocity = list(value)

class GravEntity(Entity):
    """Specialized entity for gravitational simulations."""
    pass
