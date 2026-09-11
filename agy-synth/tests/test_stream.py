import json
import os
import subprocess
import sys

from agy_synth.stream import G_LOCAL, make_sample


def test_lift_force_uses_local_gravity() -> None:
    sample = make_sample(step=0, mass_kg=2.0)

    assert sample["lift_force_n"] == 2.0 * G_LOCAL


def test_seeded_temperature_is_reproducible() -> None:
    import random

    random.seed(7)
    first = make_sample(step=1, mass_kg=10.0)

    random.seed(7)
    second = make_sample(step=1, mass_kg=10.0)

    assert first == second


def test_count_mode_emits_exactly_five_samples() -> None:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = "src"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "agy_synth.stream",
            "--count",
            "5",
            "--interval",
            "0",
            "--seed",
            "42",
        ],
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )

    samples = [json.loads(line) for line in result.stdout.splitlines()]

    assert len(samples) == 5
