import tracemalloc
from ez_grav import PhysicsState

def test_physics_tick_memory_stability():
    tracemalloc.start()
    
    state = PhysicsState(coil_temp_c=25.0, ambient_temp_c=20.0, cooling_rate=0.1)
    dt = 1.0 / 10_000
    
    # Snapshot 1: Baseline after object creation
    snapshot1 = tracemalloc.take_snapshot()
    
    # Run 100k ticks (10 seconds of simulated time)
    for _ in range(100_000):
        state.tick(dt=dt)
        
    # Snapshot 2: After high-frequency execution
    snapshot2 = tracemalloc.take_snapshot()
    
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    # We look for the top memory growth. 
    # In a stable loop, growth should be negligible (near 0).
    top_growth = stats[0].size_diff
    
    print(f"\n[MEMORY AUDIT] Peak growth in top allocation: {top_growth} bytes")
    
    tracemalloc.stop()
    
    # Fail if the top allocation grew by more than 1KB (allowing for small Python overhead)
    assert top_growth < 1024, f"Potential memory leak detected: {top_growth} bytes growth"

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
