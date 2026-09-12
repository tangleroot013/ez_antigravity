import pytest
import json
import os
import numpy as np
from src.ez_antigravity.grav_engine import CommandGravEngine

def get_chaos_samples():
    sample_dir = "tests/real_world_samples"
    samples = []
    if not os.path.exists(sample_dir):
        return samples
    for filename in os.listdir(sample_dir):
        if filename.endswith(".json"):
            with open(os.path.join(sample_dir, filename), 'r') as f:
                samples.append((filename, json.load(f)))
    return samples

@pytest.mark.parametrize("name, data", get_chaos_samples())
def test_engine_survives_chaos(name, data):
    """Ensure CommandGravEngine does not crash or leak NaNs when fed adversarial samples."""
    try:
        # Initialize the Apex engine
        engine = CommandGravEngine()
        
        # Attempt to inject chaos data into the engine state
        # We use setattr or direct assignment based on common patterns
        if "mass" in data:
            setattr(engine, 'mass', data["mass"])
        if "dist" in data:
            setattr(engine, 'distance', data["dist"])
        if "vel" in data:
            setattr(engine, 'velocity', data["vel"])

        # Trigger the calculation
        result = engine.compute_step() 
        
        # OPSEC Check: Result must be finite
        # We convert to numpy array to ensure we catch NaNs in any return type
        res_array = np.array(result)
        assert not np.isnan(res_array).any(), f"Chaos sample {name} produced NaN!"
        assert not np.isinf(res_array).any(), f"Chaos sample {name} produced Infinity!"
        
    except Exception as e:
        pytest.fail(f"Engine crashed on {name} with error: {type(e).__name__}: {e}")
