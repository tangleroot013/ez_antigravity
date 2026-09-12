import math
import pytest
from ez_antigravity.entities import GravEntity
from ez_antigravity.nbody_engine import NBodyEngine

def test_figure_eight_energy_conservation():
    engine = NBodyEngine(G=1.0, epsilon=0.0)
    p1, p2, p3 = (0.97000436, -0.24308753, 0.0), (-0.97000436, 0.24308753, 0.0), (0.0, 0.0, 0.0)
    v3 = (-0.93240737, -0.86473146, 0.0)
    v1 = (-0.5 * v3[0], -0.5 * v3[1], 0.0)
    v2 = v1
    engine.add_entity(GravEntity(id=1, mass=1.0, pos=p1, vel=v1))
    engine.add_entity(GravEntity(id=2, mass=1.0, pos=p2, vel=v2))
    engine.add_entity(GravEntity(id=3, mass=1.0, pos=p3, vel=v3))

    e_initial = engine.calculate_total_energy()
    dt = 0.001
    for _ in range(1000):
        engine.update(dt)
    
    e_final = engine.calculate_total_energy()
    relative_error = abs((e_final - e_initial) / e_initial)
    
    assert relative_error < 1e-6, f"Energy leak detected! Error: {relative_error}"

if __name__ == "__main__":
    pytest.main([__file__])
