import math

from src.ez_grav import (
    EARTH_MASS,
    EARTH_RADIUS,
    G_CONST,
    GravEngine,
    PhysicsState,
)


def test_initial_physics_state():
    engine = GravEngine(PhysicsState(mass_kg=70.0),  zero_g=False)

    assert engine.state.mass_kg == 70.0
    assert engine.state.zero_g_mode is False
    assert engine.state.altitude_m == 0.0
    assert engine.get_lift_force() == 0.0


def test_zero_g_lift_calculation():
    engine = GravEngine(PhysicsState(mass_kg=80.0),  zero_g=True)

    assert engine.calculate_lift_force() == 0.0


def test_negative_mass_tensor_flip():
    engine = GravEngine(PhysicsState(mass_kg=70.0),  zero_g=False)
    engine.toggle_negative_mass(True)

    assert engine.state.is_negative_mass is True
    assert engine.calculate_lift_force() == -1372.931


def test_orbital_velocity_calculation():
    engine = GravEngine(PhysicsState(mass_kg=70.0))

    actual = engine.calculate_orbital_velocity(altitude_km=400.0)
    expected = round(
        math.sqrt(
            (G_CONST * EARTH_MASS)
            / (EARTH_RADIUS + 400_000.0)
        ),
        2,
    )

    assert actual == expected
    assert actual == 7672.58


def test_thermal_cooling_tick():
    state = PhysicsState(mass_kg=70.0, coil_temp_c=50.0,
        cooling_rate=0.2)

    logs = state.tick(dt=1.0)

    assert abs(state.coil_temp_c - 44.0) < 0.001
    assert logs == []


def test_overheat_emergency_cutoff():
    state = PhysicsState(mass_kg=70.0, coil_temp_c=99.5,
        altitude_m=1000.0,
        zero_g_mode=True)

    logs = state.tick(dt=1.0)

    assert state.coil_temp_c == 99.0
    assert state.altitude_m == 0.0
    assert state.zero_g_mode is False

