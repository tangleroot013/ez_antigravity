import pytest
from src.ez_grav import (
    EARTH_MASS,
    EARTH_RADIUS,
    G_CONST,
    GravEngine,
)

def test_negative_mass_physics_contract():
    """Verifies sign-flip behavior and local gravity consistency."""
    # 70kg at 100m altitude
    engine = GravEngine()
    engine.state.mass_kg = 70.0
    engine.state.altitude_m = 100.0
    engine.state.is_negative_mass = True
    engine.state.zero_g_mode = False
    
    result = engine.calculate_lift_force()

    radius_m = EARTH_RADIUS + engine.state.altitude_m
    expected_magnitude = (
        G_CONST
        * EARTH_MASS
        * engine.state.mass_kg
        / radius_m**2
    )

    assert result < 0
    assert abs(result) == pytest.approx(
        expected_magnitude,
        abs=0.01,
    )

def test_zero_g_override():
    engine = GravEngine()
    engine.state.zero_g_mode = True
    assert engine.calculate_lift_force() == 0.0

def test_altitude_zero_guard():
    engine = GravEngine()
    engine.state.altitude_m = 0.0
    assert engine.calculate_lift_force() == 0.0
