import inspect
from ez_antigravity.nbody_engine import NBodyEngine

def test_integrator_signature():
    """Ensure the integrator follows the (state, dt, derivatives_fn) contract."""
    sim = NBodyEngine()
    sig = inspect.signature(sim.integrator.step)
    params = list(sig.parameters.keys())
    
    expected = ["state", "dt", "derivatives_fn"]
    
    assert params == expected, f"Integrator API mismatch! Expected {expected}, got {params}"

if __name__ == "__main__":
    # Allow running the file directly for quick verification
    import pytest
    pytest.main([__file__])
