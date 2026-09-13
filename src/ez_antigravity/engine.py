"""Core physics engine for the ez_antigravity package.

Provides the NBodyEngine that the test‑suite expects:
- add_entity
- calculate_accelerations
- get_total_momentum
- calculate_total_energy
- update (delegates to the injected integrator)

Also re‑exports GravEngine for backward‑compatible imports:
    from ez_antigravity.engine import GravEngine
"""

from typing import List, Tuple, Optional
from .entities import GravEntity
from .integrators import FastEuler, PreciseRK4  # noqa: F401
from .grav_engine import GravEngine   # <-- re‑export

Vector = Tuple[float, float, float]


class NBodyEngine:
    """A minimal N‑body simulator used by the test suite."""

    def __init__(self, G: float = 1.0, epsilon: float = 0.0,
                 integrator: Optional[object] = None):
        self.G = G                # Gravitational constant for the toy universe
        self.epsilon = epsilon    # Softening factor to avoid singularities
        self.entities: List[GravEntity] = []
        # Default to a simple Euler integrator if none supplied
        self.integrator = integrator or FastEuler()

    # ------------------------------------------------------------------ #
    # Entity management
    # ------------------------------------------------------------------ #
    def add_entity(self, entity: GravEntity) -> None:
        """Append a GravEntity to the simulation."""
        self.entities.append(entity)

    # ------------------------------------------------------------------ #
    # Physics helpers
    # ------------------------------------------------------------------ #
    def _pairwise_force(self, i: int, j: int) -> Vector:
        """Gravitational acceleration on i caused by j."""
        pi = self.entities[i].pos
        pj = self.entities[j].pos
        dx = pj[0] - pi[0]
        dy = pj[1] - pi[1]
        dz = pj[2] - pi[2]
        r2 = dx*dx + dy*dy + dz*dz + self.epsilon**2
        r = r2**0.5
        factor = self.G * self.entities[j].mass / (r2 * r)  # G*m_j / r³
        return (dx * factor, dy * factor, dz * factor)

    def calculate_accelerations(self) -> List[Vector]:
        """Return a list of acceleration vectors, one per entity."""
        n = len(self.entities)
        acc: List[Vector] = [(0.0, 0.0, 0.0) for _ in range(n)]

        for i in range(n):
            ax = ay = az = 0.0
            for j in range(n):
                if i == j:
                    continue
                fx, fy, fz = self._pairwise_force(i, j)
                ax += fx
                ay += fy
                az += fz
            acc[i] = (ax, ay, az)
        return acc

    def get_total_momentum(self) -> Vector:
        """Σ m_i * v_i for all entities."""
        mx = my = mz = 0.0
        for e in self.entities:
            mx += e.mass * e.vel[0]
            my += e.mass * e.vel[1]
            mz += e.mass * e.vel[2]
        return (mx, my, mz)

    def calculate_total_energy(self) -> float:
        """Kinetic + potential energy of the system."""
        kinetic = sum(
            0.5 * e.mass *
            (e.vel[0]**2 + e.vel[1]**2 + e.vel[2]**2)
            for e in self.entities
        )

        potential = 0.0
        n = len(self.entities)
        for i in range(n):
            for j in range(i + 1, n):
                pi = self.entities[i].pos
                pj = self.entities[j].pos
                dx = pj[0] - pi[0]
                dy = pj[1] - pi[1]
                dz = pj[2] - pi[2]
                r = (dx*dx + dy*dy + dz*dz + self.epsilon**2) ** 0.5
                potential -= self.G * \
                    self.entities[i].mass * self.entities[j].mass / r
        return kinetic + potential

    # ------------------------------------------------------------------ #
    # Integration step
    # ------------------------------------------------------------------ #
    def update(self, dt: float) -> None:
        """Advance the simulation by dt using the configured integrator."""
        positions = [tuple(e.pos) for e in self.entities]
        velocities = [tuple(e.vel) for e in self.entities]

        new_pos, new_vel = self.integrator.step(
            self, positions, velocities, dt)

        for ent, p, v in zip(self.entities, new_pos, new_vel):
            ent.pos = p
            ent.vel = v


# Export for test compatibility
__all__ = ["NBodyEngine", "GravEngine"]
