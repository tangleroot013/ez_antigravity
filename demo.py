import sys
from pathlib import Path

# ------------------------------------------------------------------
# Ensure the local src directory is on PYTHONPATH
# ------------------------------------------------------------------
workspace_root = Path(__file__).resolve().parent
src_dir = workspace_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# ------------------------------------------------------------------
# Import the library components we need.
# ------------------------------------------------------------------
try:
    from ez_antigravity.nbody_engine import NBodyEngine
    from ez_antigravity.entities import GravEntity
    from ez_antigravity.integrators import PreciseRK4
except ImportError as err:
    print(f"❌ Import error: {err}")
    print(f"Checked PYTHONPATH entry: {src_dir}")
    sys.exit(1)

def run_demo():
    print("🦆 Initializing ez_antigravity N‑Body Simulation...")

    # Setup integrator and engine
    integrator = PreciseRK4(dt=0.01)
    engine = NBodyEngine(G=6.67430e-11, integrator=integrator)

    # Create celestial entities (mass supplied directly – no EARTH_MASS constant needed)
    sun = GravEntity(
        id="sun",
        name="Sun",
        mass=1.989e30,
        position=[0.0, 0.0, 0.0],
        velocity=[0.0, 0.0, 0.0]
    )
    earth = GravEntity(
        id="earth",
        name="Earth",
        mass=5.972e24,
        position=[1.496e11, 0.0, 0.0],
        velocity=[0.0, 29780.0, 0.0]
    )

    engine.add_entity(sun)
    engine.add_entity(earth)

    print(f"🌍 Simulation started with {len(engine.entities)} entities.")

    # Run for a few steps
    steps = 5
    dt = 3600.0  # 1‑hour steps
    for step in range(steps):
        engine.step(dt)
        print(f"Step {step+1}: Earth position -> {earth.position}")

    print("✨ Simulation completed successfully! Quack!")

if __name__ == "__main__":
    run_demo()
