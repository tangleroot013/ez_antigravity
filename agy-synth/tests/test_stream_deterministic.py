import pytest
import random
from freezegun import freeze_time
from agy_synth.stream import make_sample

@freeze_time("2026-09-11 12:00:00")
def test_seeded_temperature_is_reproducible():
    seed = 42
    step = 1
    mass = 70.0
    
    # Create two independent RNGs with the same seed
    rng1 = random.Random(seed)
    rng2 = random.Random(seed)
    
    # Inject the frozen clock via freezegun's magic and the local RNGs
    # Since freezegun mocks datetime.now, our default clock lambda will be frozen
    sample1 = make_sample(step, mass, rng=rng1)
    sample2 = make_sample(step, mass, rng=rng2)
    
    assert sample1 == sample2, "Samples should be identical when seed and time are frozen!"
    print("Determinism achieved. Quack!")

if __name__ == "__main__":
    pytest.main([__file__])
