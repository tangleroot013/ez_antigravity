import tracemalloc
import pytest
from ez_grav import PhysicsState

def test_physics_tick_memory_neutrality():
    tracemalloc.start()
    
    state = PhysicsState(coil_temp_c=25.0, ambient_temp_c=20.0, cooling_rate=0.1)
    dt = 1.0 / 10_000
    
    # Warm-up: Run a few ticks to settle the Python interpreter
    for _ in range(100):
        state.tick(dt=dt)
        
    snapshot1 = tracemalloc.take_snapshot()
    
    # Stress: 100k ticks
    for _ in range(100_000):
        state.tick(dt=dt)
        
    snapshot2 = tracemalloc.take_snapshot()
    tracemalloc.stop()
    
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    top_growth = stats[0].size_diff
    
    print(f"\n[MEMORY AUDIT] Top allocation growth: {top_growth} bytes")
    
    # In a perfectly neutral loop, growth should be 0. 
    # We allow 1KB for incidental Python internal book-keeping.
    assert top_growth < 1024, f"Memory leak detected: {top_growth} bytes growth"

if __name__ == "__main__":
    pytest.main([__file__])
