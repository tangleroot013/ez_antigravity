import argparse
import json
import math
import random
import time
from datetime import datetime, timezone

G_LOCAL = 9.80665


def make_sample(step: int, mass_kg: float) -> dict:
    altitude_m = 1000.0 + math.sin(step / 10.0) * 25.0
    coil_temperature_k = 300.0 + random.uniform(-0.5, 0.5)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mass_kg": mass_kg,
        "altitude_m": altitude_m,
        "coil_temperature_k": coil_temperature_k,
        "lift_force_n": mass_kg * G_LOCAL,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--mass", type=float, default=1000.0)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    if args.interval <= 0:
        parser.error("--interval must be greater than zero")
    if args.mass < 0:
        parser.error("--mass must not be negative")

    if args.seed is not None:
        random.seed(args.seed)

    step = 0

    while True:
        print(
            json.dumps(make_sample(step, args.mass)),
            flush=True,
        )
        step += 1
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
