"""Numerical Integration Strategies for ez_grav Engine."""

from abc import ABC, abstractmethod
from typing import Callable, Tuple

AccelFn = Callable[[float, float], float]


class IntegratorStrategy(ABC):
    @abstractmethod
    def step(
        self, pos: float, vel: float, accel_fn: AccelFn, dt: float
    ) -> Tuple[float, float]:
        pass


class FastEuler(IntegratorStrategy):
    def step(
        self, pos: float, vel: float, accel_fn: AccelFn, dt: float
    ) -> Tuple[float, float]:
        acc = accel_fn(pos, vel)
        return pos + vel * dt, vel + acc * dt


class PreciseRK4(IntegratorStrategy):
    def step(
        self, pos: float, vel: float, accel_fn: AccelFn, dt: float
    ) -> Tuple[float, float]:
        k1_v = accel_fn(pos, vel)
        k1_p = vel
        k2_v = accel_fn(pos + 0.5 * dt * k1_p, vel + 0.5 * dt * k1_v)
        k2_p = vel + 0.5 * dt * k1_v
        k3_v = accel_fn(pos + 0.5 * dt * k2_p, vel + 0.5 * dt * k2_v)
        k3_p = vel + 0.5 * dt * k2_v
        k4_v = accel_fn(pos + dt * k3_p, vel + dt * k3_v)
        k4_p = vel + dt * k3_v
        new_pos = pos + (dt / 6.0) * (k1_p + 2.0 * k2_p + 2.0 * k3_p + k4_p)
        new_vel = vel + (dt / 6.0) * (k1_v + 2.0 * k2_v + 2.0 * k3_v + k4_v)
        return new_pos, new_vel
