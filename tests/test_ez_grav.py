def test_negative_mass_tensor_flip():
    from ez_antigravity.grav_engine import GravEngine
    engine = GravEngine(mass_kg=70.0, zero_g=False)
    engine.toggle_negative_mass(True)
    assert engine.state.is_negative_mass is True
    lift = engine.calculate_lift_force()
    # The expected lift force is -2 * mass * g_standard
    g_standard = 9.80665
    expected_lift = -2.0 * 70.0 * g_standard
    assert abs(lift - expected_lift) < 1e-3, f"Expected lift ~{expected_lift}, got {lift}"
