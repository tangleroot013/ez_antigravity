import time

def make_sample(seed, clock=time.time):
    # Simulated sample generation using a timestamp
    now = clock()
    return f"sample_{seed}_{now}"

def test_determinism():
    seed = 42
    # Inject a frozen clock
    frozen_clock = lambda: 1600000000.0
    
    sample1 = make_sample(seed, clock=frozen_clock)
    sample2 = make_sample(seed, clock=frozen_clock)
    
    assert sample1 == sample2, "Samples should be identical with a frozen clock!"
    print("Determinism verified. Quack!")

if __name__ == "__main__":
    test_determinism()
