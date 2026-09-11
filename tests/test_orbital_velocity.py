import math

from ez_grav import EARTH_MASS, EARTH_RADIUS, G_CONST, GravEngine


def test_orbital_velocity_calculation():
    engine = GravEngine()

    expected = round(
        math.sqrt(
            (G_CONST * EARTH_MASS)
            / (EARTH_RADIUS + 400_000.0)
        ),
        2,
    )

    assert engine.calculate_orbital_velocity(400.0) == expected
