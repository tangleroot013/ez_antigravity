class FastEuler:
    def step(self, engine, dt):
        # Basic Euler integration: pos = pos + v*dt
        positions = [e.position for e in engine.entities]
        accels = engine.calculate_accelerations(positions)
        for i, entity in enumerate(engine.entities):
            for axis in range(3):
                entity.velocity[axis] += accels[i][axis] * dt
                entity.position[axis] += entity.velocity[axis] * dt

class PreciseRK4:
    def step(self, engine, dt):
        # 4th Order Runge-Kutta for high-precision orbits
        entities = engine.entities
        initial_pos = [list(e.position) for e in entities]
        initial_vel = [list(e.velocity) for e in entities]
        
        def get_accel(pos_state):
            return engine.calculate_accelerations(pos_state)

        # k1
        v1 = initial_vel
        a1 = get_accel(initial_pos)

        # k2
        pos2 = [[p[i] + v1[j][i] * dt/2 for i in range(3)] for j, p in enumerate(initial_pos)]
        v2 = [[v[i] + a1[j][i] * dt/2 for i in range(3)] for j, v in enumerate(initial_vel)]
        a2 = get_accel(pos2)

        # k3
        pos3 = [[p[i] + v2[j][i] * dt/2 for i in range(3)] for j, p in enumerate(initial_pos)]
        v3 = [[v[i] + a2[j][i] * dt/2 for i in range(3)] for j, v in enumerate(initial_vel)]
        a3 = get_accel(pos3)

        # k4
        pos4 = [[p[i] + v3[j][i] * dt for i in range(3)] for j, p in enumerate(initial_pos)]
        v4 = [[v[i] + a3[j][i] * dt for i in range(3)] for j, v in enumerate(initial_vel)]
        a4 = get_accel(pos4)

        # Final Update
        for i, e in enumerate(entities):
            for axis in range(3):
                e.position[axis] += (dt/6) * (v1[i][axis] + 2*v2[i][axis] + 2*v3[i][axis] + v4[i][axis])
                e.velocity[axis] += (dt/6) * (a1[i][axis] + 2*a2[i][axis] + 2*a3[i][axis] + a4[i][axis])
