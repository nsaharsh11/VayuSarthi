"""Active domain contracts and validation."""
import pytest

from vayu.schemas import Tail, Spare, Resource, PlanningState, canonical_json


def test_contract_and_canonical_encoding():
    tail = Tail('T1', 10, 8, 12, 2, 3)
    state = PlanningState((tail,), (Spare('S1', 0),), (Resource('B1'),), (Resource('C1'),))
    assert canonical_json(state) == canonical_json(state)
    assert not {'truth', 'true_rul', 'failure_cycle'} & set(tail.__dataclass_fields__)
    with pytest.raises(TypeError):
        Tail('T1', 10, 8, 12, 2, 3, true_rul=9)


@pytest.mark.parametrize('values', [(10, 11, 12, 1, 3), (10, 8, 9, 1, 3),
                                    (10, 8, 12, 0, 3), (10, 8, 12, 1, 0),
                                    (float('nan'), 8, 12, 1, 3)])
def test_invalid_tail(values):
    with pytest.raises(ValueError):
        Tail('T1', *values)


def test_duplicate_resource_rejected():
    with pytest.raises(ValueError):
        PlanningState((), (), (Resource('B'), Resource('B')), (Resource('C'),))
