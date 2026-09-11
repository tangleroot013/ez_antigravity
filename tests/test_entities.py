import pytest

from ez_antigravity.entities import GravEntity


def test_kinetic_energy():
    entity = GravEntity(
        name="probe",
        mass=2.0,
        position=[0.0, 0.0, 0.0],
        velocity=[3.0, 4.0, 0.0],
    )

    assert entity.kinetic_energy == pytest.approx(25.0)


def test_update_position():
    entity = GravEntity(
        name="probe",
        mass=1.0,
        position=[1.0, 2.0, 3.0],
        velocity=[10.0, -2.0, 0.5],
    )

    entity.update_position(0.2)

    assert entity.position == pytest.approx([3.0, 1.6, 3.1])
    assert entity.velocity == [10.0, -2.0, 0.5]


def test_dimension_mismatch_is_rejected():
    with pytest.raises(ValueError, match="3-dimensional vectors"):
        GravEntity("invalid", 1.0, [0.0, 0.0], [0.0])


def test_negative_mass_is_rejected():
    with pytest.raises(ValueError, match="cannot be negative"):
        GravEntity("invalid", -1.0, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
