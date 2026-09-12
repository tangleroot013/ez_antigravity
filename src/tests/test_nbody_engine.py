import math

from ez_antigravity.entities import GravEntity
from ez_antigravity.nbody_engine import NBodyEngine


def test_two_body_accelerations_are_equal_and_opposite_in_force():
    engine = NBodyEngine(G=1.0, epsilon=0.0)

    engine.add_entity(
        GravEntity(id=1, mass=2.0, pos=(0.0, 0.0, 0.0))
    )
    engine.add_entity(
        GravEntity(id=2, mass=3.0, pos=(1.0, 0.0, 0.0))
    )

    accelerations = engine.calculate_accelerations(
        [entity.pos for entity in engine.entities]
    )

    a1, a2 = accelerations

    assert math.isclose(a1[0], 3.0)
    assert math.isclose(a2[0], -2.0)
    assert math.isclose(2.0 * a1[0] + 3.0 * a2[0], 0.0)


def test_total_momentum_is_initially_zero():
    engine = NBodyEngine(G=1.0, epsilon=0.01)

    engine.add_entity(
        GravEntity(id=1, mass=1.0, vel=(1.0, 0.0, 0.0))
    )
    engine.add_entity(
        GravEntity(id=2, mass=1.0, vel=(-1.0, 0.0, 0.0))
    )

    assert engine.get_total_momentum() == (0.0, 0.0, 0.0)
