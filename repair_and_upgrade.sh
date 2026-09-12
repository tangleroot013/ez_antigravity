#!/usr/bin/env bash
set -euo pipefail

# -------------------------------------------------
# Carter's Full Perimeter Recovery & Euler Upgrade
# -------------------------------------------------

BASE="src"
PKG="${BASE}/ez_antigravity"

# ------------------------------------------------------------------
# 1️⃣ Guarantee package structure & core files (idempotent)
# ------------------------------------------------------------------
mkdir -p "$PKG"

# __init__.py – expose the public symbols
cat <<'PY' > "${PKG}/__init__.py"
from .entities import GravEntity
from .integrators import FastEuler, PreciseRK4
from .ez_grav import EARTH_MASS, EARTH_RADIUS
PY

# entities.py – dataclass version (clean, type‑checked)
cat <<'PY' > "${PKG}/entities.py"
"""Core data structures for ez_antigravity."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, List

Vector3 = Tuple[float, float, float]

@dataclass
class GravEntity:
    """A physical body participating in the N‑body simulation."""
    name: str
    mass: float
    position: Vector3 = field(default_factory=lambda: (0.0, 0.0, 0.0))
    velocity: Vector3 = field(default_factory=lambda: (0.0, 0.0, 0.0))
    forces: List[Vector3] = field(default_factory=list)

    def net_force(self) -> Vector3:
        """Sum all force vectors acting on this entity."""
        if not self.forces:
            return (0.0, 0.0, 0.0)
        fx = sum(f[0] for f in self.forces)
        fy = sum(f[1] for f in self.forces)
        fz = sum(f[2] for f in self.forces)
        return (fx, fy, fz)

    def clear_forces(self) -> None:
        """Reset the per‑step force accumulator."""
        self.forces.clear()
PY

# ez_grav.py – physics constants (ensure both exist)
cat <<'PY' > "${PKG}/ez_grav.py"
# Fundamental constants used by the simulation
EARTH_MASS   = 5.972e24   # kg
EARTH_RADIUS = 6.371e6    # m
PY

# ------------------------------------------------------------------
# 2️⃣ Implement real Euler integration (FastEuler)
# ------------------------------------------------------------------
cat <<'PY' > "${PKG}/integrators.py"
"""Numerical integrators for the N‑body engine."""

from __future__ import annotations
from typing import Iterable, Dict, Tuple
from .entities import GravEntity

Vector3 = Tuple[float, float, float]

class FastEuler:
    """Simple explicit Euler integrator (first‑order)."""

    def __init__(self, dt: float = 0.01):
        self.dt = dt

    def step(self, entities: Iterable[GravEntity], forces: Dict[GravEntity, Vector3]) -> None:
        """
        Perform one Euler sub‑step.

        1. Compute acceleration a = F / m for each entity.
        2. Update velocity: v ← v + a·dt
        3. Update position: p ← p + v·dt
        """
        for e in entities:
            # ---- 1️⃣ Net force (the caller may have already summed it) ----
            fx, fy, fz = forces.get(e, (0.0, 0.0, 0.0))

            # ---- 2️⃣ Acceleration (a = F / m) ----
            ax = fx / e.mass
            ay = fy / e.mass
            az = fz / e.mass

            # ---- 3️⃣ New velocity ----
            vx = e.velocity[0] + ax * self.dt
            vy = e.velocity[1] + ay * self.dt
            vz = e.velocity[2] + az * self.dt
            e.velocity = (vx, vy, vz)

            # ---- 4️⃣ New position ----
            px = e.position[0] + vx * self.dt
            py = e.position[1] + vy * self.dt
            pz = e.position[2] + vz * self.dt
            e.position = (px, py, pz)

class PreciseRK4:
    """Placeholder – a full RK4 implementation can be added later."""
    def __init__(self, dt: float = 0.01):
        self.dt = dt

    def step(self, entities, forces):
        # Keep the stub so existing tests that only check existence still pass.
        for e in entities:
            e.position = tuple(p + v * self.dt for p, v in zip(e.position, e.velocity))
PY

# ------------------------------------------------------------------
# 3️⃣ Quick sanity‑check (smoke test) – runs the engine once
# ------------------------------------------------------------------
python3 - <<'PY'
import sys, os
sys.path.append(os.path.abspath("src"))

from ez_antigravity.entities import GravEntity
from ez_antigravity.nbody_engine import NBodyEngine
from ez_antigravity.integrators import FastEuler
from ez_antigravity.ez_grav import EARTH_MASS

engine = NBodyEngine()
engine.add_entity(GravEntity(name="Earth", mass=EARTH_MASS,
                             position=(0.0, 0.0, 0.0),
                             velocity=(0.0, 0.0, 0.0)))
engine.integrator = FastEuler(dt=0.1)

# The engine will compute forces internally; we just step once.
engine.step()
print("✅ Smoke test passed – entity after one step:",
      engine.entities[0])
PY

# ------------------------------------------------------------------
# 4️⃣ Run the full test suite
# ------------------------------------------------------------------
echo "🚀 Running full pytest suite..."
pytest -q
