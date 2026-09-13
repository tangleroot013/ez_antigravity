import math
from .constants import RHO_0, SCALE_HEIGHT, J2_CONSTANT, DRAG_COEFF, CROSS_SECTION_AREA, EARTH_MASS, G_CONST, EARTH_RADIUS  # noqa: E501


class PerturbationModel:
    """Calculates non-keplerian accelerations for real-world resilience."""

    @staticmethod
    def get_atmospheric_drag(r, v):
        """Calculates drag acceleration: a = -0.5 * rho * v^2 * Cd * A / m"""
        altitude = r - EARTH_RADIUS
        if altitude > 1000000:  # Negligible drag above 1000km
            return 0.0

        # Exponential atmospheric density model
        rho = RHO_0 * math.exp(-altitude / SCALE_HEIGHT)
        # We assume mass is 70kg for this specific calculation context
        mass = 70.0

        # Drag acts opposite to velocity vector
        # a_drag = -0.5 * rho * v * (Cd * A / m)
        accel_drag = -0.5 * rho * \
            abs(v) * (DRAG_COEFF * CROSS_SECTION_AREA / mass)
        return accel_drag

    @staticmethod
    def get_j2_perturbation(r):
        """Calculates acceleration due to Earth's oblateness (J2 effect)."""
        # Simplified J2 effect for a 1D radial projection
        # In 3D this varies by latitude, but we'll add a variance factor
        return (3/2) * J2_CONSTANT * (G_CONST * EARTH_MASS / r**2) * (EARTH_RADIUS / r)**2  # noqa: E501
