import math
import pytest
from ez_antigravity.entities import GravEntity
from ez_antigravity.nbody_engine import NBodyEngine

def test_figure_eight_stability():
    """
    Tests the famous Figure-8 3-body solution.
    Masses: m1 = m2 = m3 = 1.0
    G = 1.0
    """
    engine = NBodyEngine(G=1.0, epsilon=0.0)
    
    # Initial positions for Figure-8
    # Ref: Chenciner & Montgomery (2000)
    p1 = (0.97000436, -0.24308753, 0.0)
    p2 = (-0.97000436, 0.24308753, 0.0)
    p3 = (0.0, 0.0, 0.0)
    
    # Initial velocities
    v3 = (-0.93240737, -0.86473146, 0.0)
    v1 = (-0.5 * v3[0], -0.5 * v3[1], 0.0)
    v2 = v1 # v1 = v2 = -0.5 * v3
    
    engine.add_entity(GravEntity(id=1, mass=1.0, pos=p1, vel=v1))
    engine.add_entity(GravEntity(id=2, mass=1.0, pos=p2, vel=v2))
    engine.add_entity(GravEntity(id=3, mass=1.0, pos=p3, vel=v3))
    
    initial_momentum = engine.get_total_momentum()
    
    # Run for several steps
    dt = 0.01
    for _ in range(100):
        engine.update(dt)
        
    final_momentum = engine.get_total_momentum()
    
    # Momentum conservation check: Sum of P should be ~0
    for i in range(3):
        assert math.isclose(initial_momentum[i], final_momentum[i], abs_tol=1e-9), \
            f"Momentum drift detected in axis {i}! Quack!"

if __name__ == "__main__":
    pytest.main([__file__])
