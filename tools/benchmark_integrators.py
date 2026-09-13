from ez_antigravity.constants import G_CONST, EARTH_MASS
from ez_antigravity.grav_engine import GravEngine
from ez_antigravity.integrators import FastEuler, PreciseRK4, VerletIntegrator
import sys
import os

# Add src to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


def calculate_energy(r, v):
    # Specific energy: E = 0.5*v^2 - GM/r
    return 0.5 * v**2 - (G_CONST * EARTH_MASS) / r


def run_benchmark(integrator_cls, steps=1000, dt=0.1):
    engine = GravEngine(integrator=integrator_cls(dt))
    r, v = 6771000.0, 0.0
    e0 = calculate_energy(r, v)

    for _ in range(steps):
        r, v = engine.integrator.step((r, v), dt, engine.calculate_accelerations)

    ef = calculate_energy(r, v)
    return ef - e0, r, v


if __name__ == "__main__":
    integrators = [
        ("Euler", FastEuler),
        ("RK4", PreciseRK4),
        ("Verlet", VerletIntegrator),
    ]

    print(f"{'Integrator':<12} | {'Drift':<15} | {'Final R':<15} | {'Final V':<15}")
    print("-" * 60)

    for name, cls in integrators:
        drift, r, v = run_benchmark(cls)
        print(f"{name:<12} | {drift:<15.6e} | {r:<15.4f} | {v:<15.4f}")
