import json
import sys

import pytest

from agy_synth.stream import main as stream_main


def test_lift_force_physics_invariant() -> None:
    gravity = 9.80665
    mass_values = [50.0, 75.5, 100.25, 150.0]

    for mass in mass_values:
        expected_lift = mass * gravity
        calculated_lift = mass * 9.80665

        assert calculated_lift == expected_lift


@pytest.mark.parametrize(
    ("seed", "expected_count"),
    [
        (42, 5),
        (123, 3),
    ],
)
def test_stream_count_and_physics_payload(
    seed: int,
    expected_count: int,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "stream.py",
            "--count",
            str(expected_count),
            "--mass",
            "100",
            "--interval",
            "0",
            "--seed",
            str(seed),
        ],
    )

    assert stream_main() == 0

    captured = capsys.readouterr()
    lines = captured.out.strip().splitlines()

    assert len(lines) == expected_count

    for line in lines:
        sample = json.loads(line)

        assert "mass_kg" in sample
        assert "altitude_m" in sample
        assert "coil_temperature_k" in sample
        assert "lift_force_n" in sample

        assert 50.0 <= sample["mass_kg"] <= 150.0
        assert 100.0 <= sample["altitude_m"] <= 5000.0
        assert 295.0 <= sample["coil_temperature_k"] <= 350.0

        expected_lift = sample["mass_kg"] * 9.80665
        assert sample["lift_force_n"] == pytest.approx(expected_lift)
