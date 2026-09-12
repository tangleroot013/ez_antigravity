class Entity:
    def __init__(self, id=None, name=None, mass=1.0,
                 position=None, velocity=None,
                 pos=None, vel=None):
        # Resolve input variations – all end up as mutable lists.
        p = position if position is not None else (pos if pos is not None else [0.0, 0.0, 0.0])
        v = velocity if velocity is not None else (vel if vel is not None else [0.0, 0.0, 0.0])

        self.id = id
        self.name = name
        self.position = list(p)
        self.velocity = list(v)
        self.mass = float(mass)

    def update_position(self, dt):
        """Euler update – returns a *list* (tests expect a list, not a tuple)."""
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.position[2] += self.velocity[2] * dt
        return list(self.position)


class GravEntity(Entity):
    """Placeholder subclass – currently adds no extra behaviour."""
    pass
