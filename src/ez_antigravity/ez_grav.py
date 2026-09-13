G = 6.67430e-11
GRAVITATIONAL_CONSTANT = 6.67430e-11
G_CONST = 6.67430e-11
EARTH_MASS = 5.972e24
SUN_MASS = 1.989e30
EARTH_RADIUS = 6.371e6
AU = 1.496e11

__all__ = [
    "G",
    "GRAVITATIONAL_CONSTANT",
    "G_CONST",
    "EARTH_MASS",
    "SUN_MASS",
    "EARTH_RADIUS",
    "AU",
    "GravEngineState",
    "GravEngine",
]


class GravEngineState:
    """State container for GravEngine."""

    def __init__(self):
        self.mass_kg = 70.0
        self.altitude_m = 100.0
        self.is_negative_mass = False
        self.zero_g_mode = False


class GravEngine:
    """Anti-gravity and gravitational physics engine."""

    def __init__(self, mass_kg=70.0, zero_g=False, integrator=None, *args, **kwargs):  # noqa: E501
        self.integrator = integrator
        self.state = GravEngineState()
        self.state.mass_kg = mass_kg
        self.state.zero_g_mode = zero_g
        self.state.altitude_m = 100.0

    def toggle_negative_mass(self, val: bool):
        self.state.is_negative_mass = val

    def calculate_lift_force(self):
        if self.state.zero_g_mode or self.state.altitude_m == 0.0:
            return 0.0

        # Real physics: F = G * (m1 * m2) / r^2
        radius_m = EARTH_RADIUS + self.state.altitude_m
        force = (G_CONST * EARTH_MASS * self.state.mass_kg) / (radius_m**2)

        if self.state.is_negative_mass:
            return -force
        return force
