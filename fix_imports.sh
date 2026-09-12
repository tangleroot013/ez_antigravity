#!/usr/bin/env bash
set -euo pipefail

# -------------------------------------------------------------
# 1️⃣  Write constants.py
# -------------------------------------------------------------
cat > src/ez_antigravity/constants.py <<'EOF'
"""Physical constants for the ez_antigravity package.
These are imported by every other module, so they must **not** import
any other ez_antigravity code – that’s what breaks the circular import.
"""

# Fundamental
G_CONST = 6.67430e-11          # m³·kg⁻¹·s⁻²
LIGHT_SPEED = 299_792_458.0   # m·s⁻¹
AU = 1.495_978_707e11         # astronomical unit, m

# Solar system bodies
SUN_MASS = 1.988_47e30        # kg
SUN_RADIUS = 6.963_40e8       # m

EARTH_MASS = 5.972_2e24       # kg
EARTH_RADIUS = 6.371_0e6      # m

MOON_MASS = 7.342e22          # kg
MOON_RADIUS = 1.737_4e6       # m

MARS_MASS = 6.417_1e23        # kg
MARS_RADIUS = 3.389_5e6       # m

JUPITER_MASS = 1.898_2e27     # kg
JUPITER_RADIUS = 6.991_1e7    # m

# Unit conversion helpers
KM_TO_M = 1_000.0
M_TO_KM = 0.001
DAY_TO_SEC = 86_400.0
HOUR_TO_SEC = 3_600.0

# Engine defaults
DEFAULT_TIME_STEP = 60.0          # s
DEFAULT_SOFTENING = 1.0e-9        # m (softening length)
EOF

# -------------------------------------------------------------
# 2️⃣  Write utils.py (pure‑math helpers)
# -------------------------------------------------------------
cat > src/ez_antigravity/utils.py <<'EOF'
"""Standalone physics helper functions for the N‑body engine.
They depend only on :pymod:`ez_antigravity.constants` so they stay
independent of the engine implementation.
"""

import math
from .constants import G_CONST, DEFAULT_SOFTENING

def compute_gravitational_force(m1: float, m2: float,
                                distance: float,
                                softening: float = DEFAULT_SOFTENING) -> float:
    """Return the magnitude of the Newtonian gravitational force."""
    r_sq = distance * distance + softening * softening
    return G_CONST * m1 * m2 / r_sq


def compute_orbital_velocity(central_mass: float, radius: float) -> float:
    """Circular orbital speed for a body at *radius* around *central_mass*."""
    if radius <= 0:
        return 0.0
    return math.sqrt(G_CONST * central_mass / radius)


def compute_escape_velocity(central_mass: float, radius: float) -> float:
    """Escape velocity from a spherical body of *central_mass* at *radius*."""
    if radius <= 0:
        return 0.0
    return math.sqrt(2.0 * G_CONST * central_mass / radius)
EOF

# -------------------------------------------------------------
# 3️⃣  Patch ez_grav.py – import constants only; keep engine import
# -------------------------------------------------------------
cat > src/ez_antigravity/ez_grav.py <<'EOF'
"""High‑level gravity helpers and the public *GravEngine* alias.

We import :class:`NBodyEngine` **after** pulling constants so the
module graph becomes:

constants ─► utils ─► nbody_engine ─► ez_grav
"""

from .constants import (
    G_CONST, LIGHT_SPEED, AU,
    SUN_MASS, SUN_RADIUS,
    EARTH_MASS, EARTH_RADIUS,
    MOON_MASS, MOON_RADIUS,
    MARS_MASS, MARS_RADIUS,
    JUPITER_MASS, JUPITER_RADIUS,
    KM_TO_M, M_TO_KM, DAY_TO_SEC, HOUR_TO_SEC,
    DEFAULT_TIME_STEP, DEFAULT_SOFTENING,
)

# Import the engine *after* constants are available – no cycle now.
from .nbody_engine import NBodyEngine as GravEngine
EOF

# -------------------------------------------------------------
# 4️⃣  Patch nbody_engine.py – pull constants from leaf module only
# -------------------------------------------------------------
cat > src/ez_antigravity/nbody_engine.py <<'EOF'
"""Core N‑body integration engine.

Only imports from :pymod:`ez_antigravity.constants` to stay
independent of higher‑level wrappers.
"""

from .constants import G_CONST, DEFAULT_SOFTENING

class NBodyEngine:
    """Base engine used by :class:`ez_antigravity.ez_grav.GravEngine`.

    The constructor mirrors the original signature but defaults
    to the global ``DEFAULT_SOFTENING`` constant.
    """

    def __init__(self, softening: float = DEFAULT_SOFTENING, **kwargs):
        self.softening = softening
        # Store any additional state that subclasses may need.
        self.state = type('State', (), {})()
        for k, v in kwargs.items():
            setattr(self.state, k, v)

    # Existing integration methods stay untouched –
    # they can reference G_CONST or self.softening as before.
EOF

# -------------------------------------------------------------
# 5️⃣  (Re)install the package in editable mode so Python sees the new files
# -------------------------------------------------------------
python -m pip install -e .

# -------------------------------------------------------------
# 6️⃣  Run the test suite (optional – you can skip this line)
# -------------------------------------------------------------
pytest -q
