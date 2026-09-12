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
