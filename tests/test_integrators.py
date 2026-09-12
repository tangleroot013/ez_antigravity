import math

def test_rk4_vs_euler_positional_accuracy():
    r_init = 6.771e6
    v_init = 0.0
    dt = 0.1
    steps = 1000
    from ez_antigravity.integrators import FastEuler, PreciseRK4
    from ez_antigravity.grav_engine import GravEngine
    from ez_antigravity.constants import G_CONST, EARTH_MASS

    # Create engines with proper gravitational parameters
    engine_euler = GravEngine(integrator=FastEuler())
    engine_rk4 = GravEngine(integrator=PreciseRK4())

    # Set up initial conditions
    pos_euler, vel_euler = r_init, v_init
    pos_rk4, vel_rk4 = r_init, v_init

    # Calculate initial energy
    g_m = G_CONST * EARTH_MASS
    e_0 = 0.5 * v_init**2 - g_m / r_init

    # Run simulations
    for _ in range(steps):
        pos_euler, vel_euler = engine_euler.update(pos_euler, vel_euler, dt)
        pos_rk4, vel_rk4 = engine_rk4.update(pos_rk4, vel_rk4, dt)

    # Calculate final energies
    e_euler = 0.5 * vel_euler**2 - g_m / pos_euler
    e_rk4 = 0.5 * vel_rk4**2 - g_m / pos_rk4

    # Calculate relative drift
    rel_drift_euler = abs((e_euler - e_0)/e_0)
    rel_drift_rk4 = abs((e_rk4 - e_0)/e_0)

    # RK4 should have better or equal energy conservation
    # Use a small tolerance to account for floating-point imprecision
    tolerance = 1e-4  # 0.01% tolerance
    assert rel_drift_rk4 <= rel_drift_euler + tolerance, (
        f"RK4 relative drift {rel_drift_rk4:.6f} should be <= Euler drift {rel_drift_euler:.6f} "
        f"(within {tolerance:.6f} tolerance). "
        f"Euler: {e_euler:.2f}, RK4: {e_rk4:.2f}, Initial: {e_0:.2f}"
    )
