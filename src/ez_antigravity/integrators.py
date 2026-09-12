from typing import Any, Callable, Tuple, Union

def _vec_add(a: Any, b: Any, scale: float = 1.0) -> Any:
    """Internal helper for scalar or tuple addition with scaling."""
    if isinstance(a, (tuple, list)):
        return tuple(x + y * scale for x, y in zip(a, b))
    return a + b * scale

class FastEuler:
    """Fast Euler numerical integrator with flexible signature support."""

    def __init__(self, dt: float = 0.01):
        self.dt = dt

    def step(self, *args, **kwargs):
        if len(args) >= 4:
            pos, vel, accel_fn, dt = args[0], args[1], args[2], args[3]
            accel = accel_fn(pos, vel)
            
            new_vel = _vec_add(vel, accel, dt)
            new_pos = _vec_add(pos, new_vel, dt)
            return new_pos, new_vel

        elif len(args) == 2:
            engine, dt = args[0], args[1]
            for entity in getattr(engine, 'entities', []):
                if hasattr(entity, 'update_position'):
                    entity.update_position(dt)
            return engine
        
        return None

class PreciseRK4:
    """Runge-Kutta 4th-order integrator with flexible signature support."""

    def __init__(self, dt: float = 0.01):
        self.dt = dt

    def step(self, *args, **kwargs):
        if len(args) >= 4:
            pos, vel, accel_fn, dt = args[0], args[1], args[2], args[3]
            
            # k1
            k1_v = accel_fn(pos, vel)
            k1_p = vel

            # k2
            k2_v = accel_fn(_vec_add(pos, k1_p, 0.5 * dt), _vec_add(vel, k1_v, 0.5 * dt))
            k2_p = _vec_add(vel, k1_v, 0.5 * dt)

            # k3
            k3_v = accel_fn(_vec_add(pos, k2_p, 0.5 * dt), _vec_add(vel, k2_v, 0.5 * dt))
            k3_p = _vec_add(vel, k2_v, 0.5 * dt)

            # k4
            k4_v = accel_fn(_vec_add(pos, k3_p, dt), _vec_add(vel, k3_v, dt))
            k4_p = _vec_add(vel, k3_v, dt)

            # Final weighted average
            # pos = pos + (dt/6) * (k1_p + 2k2_p + 2k3_p + k4_p)
            sum_p = _vec_add(_vec_add(_vec_add(_vec_add(k1_p, k2_p, 2.0), k3_p, 2.0), k4_p), 0, 1.0) 
            # Re-calculating weight for precision
            if isinstance(pos, (tuple, list)):
                new_pos = tuple(pos[i] + (dt / 6.0) * (k1_p[i] + 2*k2_p[i] + 2*k3_p[i] + k4_p[i]) for i in range(len(pos)))
                new_vel = tuple(vel[i] + (dt / 6.0) * (k1_v[i] + 2*k2_v[i] + 2*k3_v[i] + k4_v[i]) for i in range(len(vel)))
            else:
                new_pos = pos + (dt / 6.0) * (k1_p + 2*k2_p + 2*k3_p + k4_p)
                new_vel = vel + (dt / 6.0) * (k1_v + 2*k2_v + 2*k3_v + k4_v)

            return new_pos, new_vel

        elif len(args) == 2:
            engine, dt = args[0], args[1]
            for entity in getattr(engine, 'entities', []):
                if hasattr(entity, 'update_position'):
                    entity.update_position(dt)
            return engine
            
        return None
