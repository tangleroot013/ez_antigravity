class FastEuler:
    """Fast Euler numerical integrator with flexible signature support."""

    def __init__(self, dt=0.01):
        self.dt = dt

    def step(self, state, dt, derivatives_fn):
        pos, vel = state
        accel = derivatives_fn(pos) if callable(derivatives_fn) else derivatives_fn
        if isinstance(accel, (tuple, list)):
            if len(accel) == 2:
                new_vel = (vel[0] + accel[0] * dt, vel[1] + accel[1] * dt)
                new_pos = (pos[0] + new_vel[0] * dt, pos[1] + new_vel[1] * dt)
                return new_pos, new_vel
            accel = accel[0]
        new_vel = vel + accel * dt
        new_pos = pos + new_vel * dt
        return new_pos, new_vel


class PreciseRK4:
    """Runge-Kutta 4th-order integrator with flexible signature support."""

    def __init__(self, dt=0.01):
        self.dt = dt

    def step(self, state, dt, derivatives_fn):
        pos, vel = state

        def f(p, v):
            a = derivatives_fn(p) if callable(derivatives_fn) else derivatives_fn
            return v, a

        k1_p, k1_v = f(pos, vel)
        k2_p, k2_v = f(pos + 0.5 * dt * k1_p, vel + 0.5 * dt * k1_v)
        k3_p, k3_v = f(pos + 0.5 * dt * k2_p, vel + 0.5 * dt * k2_v)
        k4_p, k4_v = f(pos + dt * k3_p, vel + dt * k3_v)

        new_pos = pos + (dt / 6.0) * (k1_p + 2 * k2_p + 2 * k3_p + k4_p)
        new_vel = vel + (dt / 6.0) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)
        return new_pos, new_vel

class VerletIntegrator:
    """Velocity Verlet symplectic integrator for energy conservation."""
    
    def __init__(self, dt=0.01):
        self.dt = dt

    def step(self, state, dt, derivatives_fn):
        pos, vel = state
        
        # Current acceleration
        accel_t = derivatives_fn(pos) if callable(derivatives_fn) else derivatives_fn
        
        # Position update: r(t + dt) = r(t) + v(t)dt + 0.5 * a(t)dt^2
        new_pos = pos + vel * dt + 0.5 * accel_t * (dt**2)
        
        # New acceleration based on updated position
        accel_t_plus_dt = derivatives_fn(new_pos) if callable(derivatives_fn) else derivatives_fn
        
        # Velocity update: v(t + dt) = v(t) + 0.5 * (a(t) + a(t + dt))dt
        new_vel = vel + 0.5 * (accel_t + accel_t_plus_dt) * dt
        
        return new_pos, new_vel
