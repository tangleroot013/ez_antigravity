import math
import random
import argparse
from datetime import datetime, timezone

G_LOCAL = 9.80665

def make_sample(step: int, mass_kg: float, rng=random, clock=lambda: datetime.now(timezone.utc)) -> dict:
    altitude_m = 1000.0 + math.sin(step / 10.0) * 25.0
    # Use the injected rng instead of the global random module
    coil_temperature_k = 300.0 + rng.uniform(-0.5, 0.5)

    return {
        "timestamp": clock().isoformat(),
        "mass_kg": mass_kg,
        "altitude_m": altitude_m,
        "coil_temperature_k": coil_temperature_k,
        "lift_force_n": mass_kg * G_LOCAL,
    }

def parse_args():
    # Placeholder for the rest of your file
    pass
