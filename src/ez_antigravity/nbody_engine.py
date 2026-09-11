import math
from typing import List, Tuple
from ez_antigravity.entities import GravEntity

class PreciseRK4:
    def step(self, state: List[float], dt: float, derivatives_fn) -> List[float]:
        """Performs a single 4th-order Runge-Kutta step on a flat state vector."""
        k1 = derivatives_fn(state)
        state_k2 = [s + 0.5 * dt * k for s, k in zip(state, k1)]
        k2 = derivatives_fn(state_k2)
        state_k3 = [s + 0.5 * dt * k for s, k in zip(state, k2)]
        k3 = derivatives_fn(state_k3)
        state_k4 = [s + dt * k for s, k in zip(state, k3)]
        k4 = derivatives_fn(state_k4)
        return [
            s + (dt / 6.0) * (dk1 + 2.0 * dk2 + 2.0 * dk3 + dk4)
            for s, dk1, dk2, dk3, dk4 in zip(state, k1, k2, k3, k4)
        ]

class NBodyEngine:
    def __init__(self, G: float = 1.0, epsilon: float = 0.0):
        self.G = G
        self.epsilon = epsilon
        self.entities: List[GravEntity] = []
        self.integrator = PreciseRK4()

    def add_entity(self, entity: GravEntity) -> None:
        self.entities.append(entity)

    def calculate_accelerations(
        self, positions: List[Tuple[float, float, float]]
    ) -> List[Tuple[float, float, float]]:
        """Calculates pairwise accelerations using Newton's law of universal gravitation."""
        n = len(positions)
        accelerations = [[0.0, 0.0, 0.0] for _ in range(n)]
        eps_sq = self.epsilon * self.epsilon
        for i in range(n):
            for j in range(i + 1, n):
                dx = positions[j][0] - positions[i][0]
                dy = positions[j][1] - positions[i][1]
                dz = positions[j][2] - positions[i][2]
                dist_sq = dx * dx + dy * dy + dz * dz + eps_sq
                inv_dist_cube = 1.0 / (dist_sq * math.sqrt(dist_sq))
                force_factor = self.G * inv_dist_cube
                a_i_scale = force_factor * self.entities[j].mass
                a_j_scale = force_factor * self.entities[i].mass
                accelerations[i][0] += a_i_scale * dx
                accelerations[i][1] += a_i_scale * dy
                accelerations[i][2] += a_i_scale * dz
                accelerations[j][0] -= a_j_scale * dx
                accelerations[j][1] -= a_j_scale * dy
                accelerations[j][2] -= a_j_scale * dz
        return [tuple(acc) for acc in accelerations]

    def _get_state(self) -> List[float]:
        """Flattens entity positions and velocities into a 1D state array."""
        state = []
        for e in self.entities:
            state.extend([e.pos[0], e.pos[1], e.pos[2], e.vel[0], e.vel[1], e.vel[2]])
        return state

    def _set_state(self, state: List[float]) -> None:
        """Unpacks flat state vector back into entity positions and velocities."""
        for i, e in enumerate(self.entities):
            idx = 6 * i
            e.pos = (state[idx], state[idx + 1], state[idx + 2])
            e.vel = (state[idx + 3], state[idx + 4], state[idx + 5])

    def _derivatives(self, state: List[float]) -> List[float]:
        """Computes rate of change [vx, vy, vz, ax, ay, az] for all entities."""
        n = len(self.entities)
        positions = [
            (state[6 * i], state[6 * i + 1], state[6 * i + 2])
            for i in range(n)
        ]
        accelerations = self.calculate_accelerations(positions)
        derivs = []
        for i in range(n):
            vx, vy, vz = state[6 * i + 3], state[6 * i + 4], state[6 * i + 5]
            ax, ay, az = accelerations[i]
            derivs.extend([vx, vy, vz, ax, ay, az])
        return derivs

    def update(self, dt: float) -> None:
        """Advances simulation time by dt using RK4 integration."""
        if not self.entities:
            return
        current_state = self._get_state()
        next_state = self.integrator.step(current_state, dt, self._derivatives)
        self._set_state(next_state)

    def get_total_momentum(self) -> Tuple[float, float, float]:
        """Computes current total linear momentum."""
        px = sum(e.mass * e.vel[0] for e in self.entities)
        py = sum(e.mass * e.vel[1] for e in self.entities)
        pz = sum(e.mass * e.vel[2] for e in self.entities)
        return (px, py, pz)

    def momentum_is_conserved(
        self, initial_momentum: Tuple[float, float, float], tolerance: float = 1e-10
    ) -> bool:
        """Checks if current momentum matches initial momentum within tolerance."""
        current = self.get_total_momentum()
        return all(
            math.isclose(c, i, abs_tol=tolerance)
            for c, i in zip(current, initial_momentum)
        )
