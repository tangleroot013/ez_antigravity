"""Gravitational simulation entities."""

from __future__ import annotations


class GravEntity:
    """A point mass with three-dimensional position and velocity."""

    def __init__(
        self,
        name: str,
        mass: float,
        position: list[float],
        velocity: list[float],
    ) -> None:
        mass = float(mass)

        if mass < 0:
            raise ValueError("Mass cannot be negative.")

        if len(position) != 3 or len(velocity) != 3:
            raise ValueError(
                "Position and velocity must be 3-dimensional vectors."
            )

        self.name = name
        self.mass = mass
        self.position = [float(value) for value in position]
        self.velocity = [float(value) for value in velocity]

    @property
    def kinetic_energy(self) -> float:
        """Return kinetic energy in joules."""
        velocity_squared = sum(value**2 for value in self.velocity)
        return 0.5 * self.mass * velocity_squared

    @property
    def momentum(self) -> list[float]:
        """Return the linear momentum vector in kg·m/s."""
        return [self.mass * value for value in self.velocity]

    def update_position(self, dt: float) -> None:
        """Advance position by dt seconds."""
        for index, velocity_component in enumerate(self.velocity):
            self.position[index] += velocity_component * dt

    def __repr__(self) -> str:
        return (
            f"GravEntity(name={self.name!r}, mass={self.mass!r}, "
            f"position={self.position!r}, velocity={self.velocity!r})"
        )
