class FastEuler:
    def step(self, engine, dt):
        # Basic Euler integration: pos = pos + v*dt
        positions = [e.position for e in engine.entities]
        accels = engine.calculate_accelerations(positions)
        for i, entity in enumerate(engine.entities):
            for axis in range(3):
                entity.velocity[axis] += accels[i][axis] * dt
                entity.position[axis] += entity.velocity[axis] * dt
