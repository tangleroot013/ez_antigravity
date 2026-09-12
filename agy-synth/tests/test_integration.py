
import pytest
from agy_synth.stream import Synth  # Assuming this is the main synth class
# Mocking ez_grav logic for the first atomic bridge test
def mock_ez_grav_tensor():
    return {"orbital_v": 11.2, "tensor_mass": -500.0, "status": "stable"}

def clean_sample(sample):
    return {k: v for k, v in sample.items() if k != 'timestamp'}

def physics_to_telemetry_bridge(physics_state):
    return {
        "velocity": physics_state.get("orbital_v"),
        "mass_flux": physics_state.get("tensor_mass"),
        "timestamp": "2026-09-11T00:00:00Z", 
    }

def test_grav_to_synth_flow():
    print("\nQuack! Testing the gravitational bridge...")
    # 1. Get physics data
    physics_data = mock_ez_grav_tensor()
    
    # 2. Bridge it to telemetry format
    telemetry_sample = physics_to_telemetry_bridge(physics_data)
    
    # 3. Clean it to avoid timing ghosts
    cleaned = clean_sample(telemetry_sample)
    
    # 4. Assert the contract is maintained
    assert cleaned["velocity"] == 11.2
    assert cleaned["mass_flux"] == -500.0
    assert "timestamp" not in cleaned
    print("Bridge stable. No gravitational collapse detected!")
