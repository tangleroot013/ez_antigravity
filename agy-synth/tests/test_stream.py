import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

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
