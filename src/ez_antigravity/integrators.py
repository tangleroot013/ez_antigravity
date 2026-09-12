"""Integrators used by the ez_antigravity package.

FastEuler now supports two calling conventions:
    1. step(state, dt, accel_fn)   – the classic signature.
    2. step(engine, positions, velocities, dt) – the pattern used by the test suite.
"""

from typing import Callable, List, Tuple, Union

Vector = Tuple[float, float, float]


def _vec_add(a: Union[float, Vector],
             b: Union[float, Vector],
             scale: float = 1.0) -> Union[float, Vector]:
    """Add (a + scale * b) for scalars or 3‑tuples."""
    if isinstance(a, (list, tuple)):
        return tuple(x + scale * y for x, y in zip(a, b))
    return a + scale * b


class FastEuler:
    """Fast Euler integrator with flexible signature support."""

    def __init__(self, dt: float = 0.01):
        self.dt = dt

    def step(self, *args, **kwargs):
        """
        Supported signatures:

        * step(state, dt, accel_fn)
        * step(engine, positions, velocities, dt)
        """
        # -----------------------------------------------------------------
        # Engine‑first pattern (used by the test suite)
        # -----------------------------------------------------------------
        if len(args) == 4 and not callable(args[2]):
            engine, positions, velocities, dt = args
            # Compute accelerations via the engine helper
            accelerations = engine.calculate_accelerations()
            new_positions = []
            new_velocities = []
            for pos, vel, acc in zip(positions, velocities, accelerations):
                new_vel = _vec_add(vel, acc, dt)
                new_pos = _vec_add(pos, new_vel, dt)
                new_positions.append(new_pos)
                new_velocities.append(new_vel)
            return new_positions, new_velocities

        # -----------------------------------------------------------------
        # Classic signature (state, dt, accel_fn)
        # -----------------------------------------------------------------
        if len(args) >= 4:
            pos, vel, accel_fn, dt = args[0], args[1], args[2], args[3]
            accel = accel_fn(pos, vel)

            new_vel = _vec_add(vel, accel, dt)
            new_pos = _vec_add(pos, new_vel, dt)
            return new_pos, new_vel

        # -----------------------------------------------------------------
        # Engine‑update shortcut (engine, dt) – retained for backward compat.
        # -----------------------------------------------------------------
        if len(args) == 2:
            engine, dt = args[0], args[1]
            for entity in getattr(engine, 'entities', []):
                if hasattr(entity, 'update_position'):
                    entity.update_position(dt)
            return engine

        return None


class PreciseRK4:
    """Runge‑Kutta 4th‑order integrator with flexible signature support."""

    def __init__(self, dt: float = 0.01):
        self.dt = dt

    def step(self, *args, **kwargs):
        if len(args) >= 4:
            pos, vel, accel_fn, dt = args[0], args[1], args[2], args[3]

            # k1
            k1_v = accel_fn(pos, vel)
            k1_p = vel

            # k2
            k2_v = accel_fn(_vec_add(pos, k1_p, 0.5 * dt),
                            _vec_add(vel, k1_v, 0.5 * dt))
            k2_p = _vec_add(vel, k1_v, 0.5 * dt)

            # k3
            k3_v = accel_fn(_vec_add(pos, k2_p, 0.5 * dt),
                            _vec_add(vel, k2_v, 0.5 * dt))
            k3_p = _vec_add(vel, k2_v, 0.5 * dt)

            # k4
            k4_v = accel_fn(_vec_add(pos, k3_p, dt),
                            _vec_add(vel, k3_v, dt))
            k4_p = _vec_add(vel, k3_v, dt)

            # Weighted average – handle both scalar and tuple cases
            if isinstance(pos, (list, tuple)):
                new_pos = tuple(
                    pos[i] + (dt / 6.0) *
                    (k1_p[i] + 2 * k2_p[i] + 2 * k3_p[i] + k4_p[i])
                    for i in range(len(pos))
                )
                new_vel = tuple(
                    vel[i] + (dt / 6.0) *
                    (k1_v[i] + 2 * k2_v[i] + 2 * k3_v[i] + k4_v[i])
                    for i in range(len(vel))
                )
            else:
                new_pos = pos + (dt / 6.0) * (k1_p + 2 * k2_p + 2 * k3_p + k4_p)
                new_vel = vel + (dt / 6.0) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)

            return new_pos, new_vel

        if len(args) == 2:
            engine, dt = args[0], args[1]
            for entity in getattr(engine, 'entities', []):
                if hasattr(entity, 'update_position'):
                    entity.update_position(dt)
            return engine

        return None
