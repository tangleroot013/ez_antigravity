import pytest
import os
import json
from ez_antigravity.integrators import VerletIntegrator
from ez_antigravity.grav_engine import CommandGravEngine
from ez_antigravity.perturbations import PerturbationModel
from ez_antigravity.constants import EARTH_RADIUS

def test_atmospheric_drag_altitude_cutoff():
    """Verify that drag is zero at high altitudes and present at low altitudes."""
    # High altitude (1000km+) should have 0 drag
    high_alt_r = EARTH_RADIUS + 1100000
    assert PerturbationModel.get_atmospheric_drag(high_alt_r, 100.0) == 0.0
    
    # Low altitude should have negative acceleration (drag)
    low_alt_r = EARTH_RADIUS + 10000
    drag = PerturbationModel.get_atmospheric_drag(low_alt_r, 100.0)
    assert drag < 0

def test_ground_collision_detection():
    """Verify the engine recognizes when it has hit the Earth."""
    engine = CommandGravEngine(integrator=VerletIntegrator())
    # Position exactly at or below Earth radius
    accel = engine.calculate_accelerations(EARTH_RADIUS - 1.0)
    # Our ResilientGravEngine returns -9.80665 for ground collision
    assert accel == -9.80665

def test_thrust_application():
    """Verify that active thrust changes the trajectory."""
    dt = 0.1
    state_no_thrust = (EARTH_RADIUS + 100000, 0.0)
    state_with_thrust = (EARTH_RADIUS + 100000, 0.0)
    
    # Engine 1: No thrust
    engine1 = CommandGravEngine(integrator=VerletIntegrator())
    res1 = engine1.command_update(state_no_thrust, dt)
    
    # Engine 2: Max thrust
    engine2 = CommandGravEngine(integrator=VerletIntegrator())
    engine2.controller.set_thrust(500.0)
    res2 = engine2.command_update(state_with_thrust, dt)
    
    # With positive thrust, velocity should be higher than the free-fall case
    assert res2[1] > res1[1]

def test_telemetry_persistence():
    """Verify that flight data is actually written to the JSON black box."""
    log_file = "test_flight_log.json"
    engine = CommandGravEngine(integrator=VerletIntegrator())
    engine.telemetry.filename = log_file
    
    state = (EARTH_RADIUS + 100000, 0.0)
    # Run 10 steps
    for _ in range(10):
        state = engine.command_update(state, 0.1)
    
    engine.shutdown()
    
    assert os.path.exists(log_file)
    with open(log_file, 'r') as f:
        data = json.load(f)
        assert len(data) == 10
        assert data[0]['status'] == "NOMINAL"
    
    # Cleanup
    if os.path.exists(log_file):
        os.remove(log_file)

def test_energy_conservation_verlet():
    """Verify that Verlet maintains better energy stability than Euler."""
    from ez_antigravity.integrators import FastEuler
    
    def get_final_drift(integrator_cls):
        engine = CommandGravEngine(integrator=integrator_cls(0.1))
        r, v = EARTH_RADIUS + 100000, 0.0
        # Simple energy: 0.5v^2 - GM/r
        from ez_antigravity.constants import G_CONST, EARTH_MASS
        e0 = 0.5 * v**2 - (G_CONST * EARTH_MASS) / r
        
        for _ in range(100):
            # Use a basic update to avoid drag/thrust interference for this test
            r, v = engine.integrator.step((r, v), 0.1, engine.calculate_accelerations)
            
        ef = 0.5 * v**2 - (G_CONST * EARTH_MASS) / r
        return abs(ef - e0)

    drift_euler = get_final_drift(FastEuler)
    drift_verlet = get_final_drift(VerletIntegrator)
    
    # Verlet should be more stable (lower drift) than basic Euler
    assert drift_verlet < drift_euler
