import math
import pytest
from ez_antigravity.engine import GravEngine
from ez_antigravity.integrators import FastEuler, PreciseRK4

def test_rk4_vs_euler_positional_accuracy():
    r_init = 6.771e6
    v_init = 0.0
    dt = 0.1
    steps = 1000
    engine_euler = GravEngine(integrator=FastEuler())
    engine_rk4 = GravEngine(integrator=PreciseRK4())
    pos_euler, vel_euler = r_init, v_init
    pos_rk4, vel_rk4 = r_init, v_init
    for _ in range(steps):
        pos_euler, vel_euler = engine_euler.update(pos_euler, vel_euler, dt)
        pos_rk4, vel_rk4 = engine_rk4.update(pos_rk4, vel_rk4, dt)
    g_m = engine_rk4.G * engine_rk4.mass
    e_0 = 0.5 * v_init**2 - g_m / r_init
    e_euler = 0.5 * vel_euler**2 - g_m / pos_euler
    e_rk4 = 0.5 * vel_rk4**2 - g_m / pos_rk4
    assert abs(e_rk4 - e_0) < abs(e_euler - e_0)
    assert abs(e_rk4 - e_0) < 1.0

def test_2d_circular_orbit_drift():
    r = 6.771e6
    g_m = 6.674e-11 * 5.972e24
    v_circ = math.sqrt(g_m / r)
    dt = 1.0
    steps = 1000
    def accel_2d(pos, vel):
        return -g_m * pos / (abs(pos) ** 3)
    euler = FastEuler()
    rk4 = PreciseRK4()
    pos_e, vel_e = complex(r, 0.0), complex(0.0, v_circ)
    pos_r, vel_r = complex(r, 0.0), complex(0.0, v_circ)
    for _ in range(steps):
        pos_e, vel_e = euler.step(pos_e, vel_e, accel_2d, dt)
        pos_r, vel_r = rk4.step(pos_r, vel_r, accel_2d, dt)
    assert abs(abs(pos_r) - r) < abs(abs(pos_e) - r)
    assert abs(abs(pos_r) - r) < 1.0
