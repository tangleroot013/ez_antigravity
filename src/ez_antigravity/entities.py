from typing import Union, List, Optional

class Entity:
    """Base Entity class with position, velocity, and mass."""

    def __init__(
        self, 
        id: Optional[int] = None, 
        name: Optional[Union[str, float]] = None, 
        mass: Union[float, List[float]] = 1.0, 
        position: Optional[List[float]] = None, 
        velocity: Optional[List[float]] = None, 
        pos: Optional[List[float]] = None, 
        vel: Optional[List[float]] = None
    ):
        # Handle the quirky API requirement: 
        # If name is numeric and mass is a list, swap them.
        if isinstance(name, (int, float)) and isinstance(mass, (list, tuple)):
            vel = position
            pos = mass
            mass = name
            name = None
            position = None
            velocity = None

        # Resolve position and velocity from multiple possible input keywords
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

    def update_position(self, dt: float) -> List[float]:
        """Standard linear position update."""
        for i in range(3):
            self.position[i] += self.velocity[i] * dt
        return list(self.position)

    @property
    def kinetic_energy(self) -> float:
        """Calculates scalar kinetic energy."""
        v_sq = sum(v**2 for v in self.velocity)
        return 0.5 * self.mass * v_sq

    @property
    def pos(self) -> List[float]:
        return self.position

    @pos.setter
    def pos(self, value: List[float]):
        if len(value) != 3:
            raise ValueError("Position must be 3D")
        self.position = list(value)

    @property
    def vel(self) -> List[float]:
        return self.velocity

    @vel.setter
    def vel(self, value: List[float]):
        if len(value) != 3:
            raise ValueError("Velocity must be 3D")
        self.velocity = list(value)

class GravEntity(Entity):
    """Gravitational entity subclass."""
    pass
