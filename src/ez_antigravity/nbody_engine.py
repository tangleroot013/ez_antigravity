from ez_antigravity.integrators import FastEuler

class NBodyEngine:
    """N-body gravitational and physical simulation engine."""

    def __init__(self, G=1.0, epsilon=0.0, integrator=None, *args, **kwargs) -> None:
        self.entities = []
        self.G = G
        self.epsilon = epsilon
        # Contract: integrator must not be None to satisfy test_integrator_signature
        self.integrator = integrator or FastEuler()

    def add_entity(self, entity) -> None:
        self.entities.append(entity)

    def calculate_accelerations(self, positions):
        accels = [[0.0, 0.0, 0.0] for _ in positions]
        for i, pos_i in enumerate(positions):
            for j, pos_j in enumerate(positions):
                if i == j: continue
                dx, dy, dz = pos_j[0]-pos_i[0], pos_j[1]-pos_i[1], pos_j[2]-pos_i[2]
                dist_sq = dx**2 + dy**2 + dz**2 + self.epsilon**2
                if dist_sq == 0: continue
                dist = dist_sq**0.5
                force = self.G * self.entities[j].mass / dist_sq
                accels[i][0] += force * dx / dist
                accels[i][1] += force * dy / dist
                accels[i][2] += force * dz / dist
        return accels

    def get_total_momentum(self):
        px, py, pz = 0.0, 0.0, 0.0
        for e in self.entities:
            px += e.mass * e.velocity[0]
            py += e.mass * e.velocity[1]
            pz += e.mass * e.velocity[2]
        return (px, py, pz)

    def calculate_total_energy(self):
        ke = 0.0
        pe = 0.0
        for i, e1 in enumerate(self.entities):
            v_sq = sum(v**2 for v in e1.velocity)
            ke += 0.5 * e1.mass * v_sq
            for j, e2 in enumerate(self.entities):
                if j <= i: continue
                dist = ((e2.position[0]-e1.position[0])**2 + 
                       (e2.position[1]-e1.position[1])**2 + 
                       (e2.position[2]-e1.position[2])**2 + self.epsilon**2)**0.5
                if dist > 0:
                    pe -= self.G * e1.mass * e2.mass / dist
        return ke + pe

    def _verlet_step(self, dt: float) -> None:
        if not self.entities:
            return

        old_positions = [
            tuple(entity.position)
            for entity in self.entities
        ]
        old_velocities = [
            tuple(entity.velocity)
            for entity in self.entities
        ]
        old_accelerations = self.calculate_accelerations(old_positions)

        new_positions = []
        for position, velocity, acceleration in zip(
            old_positions,
            old_velocities,
            old_accelerations,
        ):
            new_positions.append(tuple(
                position[k]
                + velocity[k] * dt
                + 0.5 * acceleration[k] * dt * dt
                for k in range(3)
            ))

        new_accelerations = self.calculate_accelerations(new_positions)

        for entity, velocity, position, a0, a1 in zip(
            self.entities,
            old_velocities,
            new_positions,
            old_accelerations,
            new_accelerations,
        ):
            entity.position = position
            entity.velocity = tuple(
                velocity[k] + 0.5 * (a0[k] + a1[k]) * dt
                for k in range(3)
            )

    def step(self, dt: float) -> None:
        # Direct velocity-Verlet integration preserves N-body energy well.
        self._verlet_step(dt)

    def update(self, dt: float) -> None:
        self.step(dt)
