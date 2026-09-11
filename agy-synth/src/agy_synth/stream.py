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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Emit synthetic GravEngine telemetry as JSON Lines."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds between samples.",
    )
    parser.add_argument(
        "--mass",
        type=float,
        default=1000.0,
        help="Vehicle mass in kilograms.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Seed for reproducible thermal noise.",
    )
    parser.add_argument(
        "--count",
        type=int,
        help="Number of samples to emit. Omit for continuous streaming.",
    )

    args = parser.parse_args()

    if args.interval <= 0:
        parser.error("--interval must be greater than zero")
    if args.mass < 0:
        parser.error("--mass must not be negative")
    if args.count is not None and args.count < 0:
        parser.error("--count must not be negative")

    return args


def main() -> int:
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    step = 0

    while args.count is None or step < args.count:
        print(
            json.dumps(make_sample(step, args.mass)),
            flush=True,
        )
        step += 1

        if args.count is None or step < args.count:
            time.sleep(args.interval)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
