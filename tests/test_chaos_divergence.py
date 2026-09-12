import math
import pytest
from ez_antigravity.entities import GravEntity
from ez_antigravity.nbody_engine import NBodyEngine

def get_figure_eight_setup():
    engine = NBodyEngine(G=1.0, epsilon=0.0)
    p1, p2, p3 = (0.97000436, -0.24308753, 0.0), (-0.97000436, 0.24308753, 0.0), (0.0, 0.0, 0.0)
    v3 = (-0.93240737, -0.86473146, 0.0)
    v1 = (-0.5 * v3[0], -0.5 * v3[1], 0.0)
    v2 = v1
    engine.add_entity(GravEntity(id=1, mass=1.0, pos=p1, vel=v1))
    engine.add_entity(GravEntity(id=2, mass=1.0, pos=p2, vel=v2))
    engine.add_entity(GravEntity(id=3, mass=1.0, pos=p3, vel=v3))
    return engine

def test_lyapunov_divergence():
    # Sim A: The Control
    sim_a = get_figure_eight_setup()
    
    # Sim B: The Perturbed (Shift p1 by 1 nanometer)
    sim_b = get_figure_eight_setup()
    p1_perturbed = (0.97000436 + 1e-9, -0.24308753, 0.0)
    sim_b.entities[0].pos = p1_perturbed
    
    dt = 0.01
    steps = 2000
    divergence_history = []
    
    for _ in range(steps):
        sim_a.update(dt)
        sim_b.update(dt)
        
        # Calculate total state distance: sum(|pos_a - pos_b|)
        dist = 0.0
        for e_a, e_b in zip(sim_a.entities, sim_b.entities):
            dx = e_a.pos[0] - e_b.pos[0]
            dy = e_a.pos[1] - e_b.pos[1]
            dz = e_a.pos[2] - e_b.pos[2]
            dist += math.sqrt(dx*dx + dy*dy + dz*dz)
        divergence_history.append(dist)
    
    initial_div = divergence_history[0]
    final_div = divergence_history[-1]
    
    print(f"\nInitial Divergence: {initial_div:.2e}")
    print(f"Final Divergence: {final_div:.2e}")
    
    # In a stable Figure-8, the divergence should grow slowly.
    # In a chaotic system, it would explode.
    assert final_div > initial_div, "The simulations didn't diverge at all! Quack!"

if __name__ == "__main__":
    pytest.main([__file__])
