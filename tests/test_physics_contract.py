import pytest
from src.ez_grav import GravEngine

def test_negative_mass_physics_contract():
    """Verifies sign-flip behavior and local gravity consistency."""
    # 70kg at 100m altitude
    engine = GravEngine()
    engine.state.mass_kg = 70.0
    engine.state.altitude_m = 100.0
    engine.state.is_negative_mass = True
    engine.state.zero_g_mode = False
    
    # Expected: - (G * M_earth * m) / (R_earth + h)^2
    # For 70kg at 100m: approx -686.46
    result = engine.calculate_lift_force()
    
    # We use a tight tolerance to ensure g_local is actually being used
    # and not just a rounded STANDARD_G
    assert result < 0
    assert abs(result) == pytest.approx(686.46, abs=0.01)

def test_zero_g_override():
    engine = GravEngine()
    engine.state.zero_g_mode = True
    assert engine.calculate_lift_force() == 0.0

def test_altitude_zero_guard():
    engine = GravEngine()
    engine.state.altitude_m = 0.0
    assert engine.calculate_lift_force() == 0.0
