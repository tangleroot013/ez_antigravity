import pytest
import json
import os
import numpy as np
# Assuming your engine is in src.ez_antigravity
try:
    from src.ez_antigravity.engine import SimulationEngine 
except ImportError:
    # Fallback for different structure
    SimulationEngine = None

def get_chaos_samples():
    sample_dir = "tests/real_world_samples"
    samples = []
    for filename in os.listdir(sample_dir):
        if filename.endswith(".json"):
            with open(os.path.join(sample_dir, filename), 'r') as f:
                samples.append((filename, json.load(f)))
    return samples

@pytest.mark.parametrize("name, data", get_chaos_samples())
def test_engine_survives_chaos(name, data):
    """Ensure the engine does not crash when fed adversarial samples."""
    if SimulationEngine is None:
        pytest.skip("SimulationEngine not found in path")
        
    # We wrap this in a try-block because the goal is to find 
    # where it crashes without stopping the whole suite
    try:
        # Initialize engine with chaos data
        # Adjust the init call to match your actual SimulationEngine signature
        engine = SimulationEngine(mass=data.get("mass", 1.0), distance=data.get("dist", 1.0))
        result = engine.compute_step() 
        
        # OPSEC Check: Result should not be NaN or Inf
        assert not np.isnan(result).any(), f"Chaos sample {name} produced NaN!"
        assert not np.isinf(result).any(), f"Chaos sample {name} produced Infinity!"
    except Exception as e:
        pytest.fail(f"Engine crashed on {name} with error: {e}")
