from math import isclose
from itertools import combinations, chain

import pytest

from lenscalc import Lens


# Create lists for parametrized tests
single_variable_passing = [("r1",), ("r2",), ("FFL",), ("BFL",), ("NPS",)]
single_variable_failing = [("D1",), ("D2",), ("D",), ("n1",), ("nL",), ("n2",), ("CT",), ("P1",), ("P2",), ("f1",), ("f2",), ("EFL",)]

pairs = combinations(Lens.variables, 2)
# itertools.combinations returns an ordered iterable,
# that is why it is possible to search by the indexes.
# To search by indexes it is needed to make it a list.
# pairs_passing_indexes = 81, 88, 89, 90, 97, 98, 99, 112, 119, 133, 134, 135
# pairs_passing = [pairs[index] for index in pairs_passing_indexes]
pairs_passing = [
    ('r1', 'r2'),
    ('r1', 'FFL'),
    ('r1', 'BFL'),
    ('r1', 'NPS'),
    ('r2', 'FFL'),
    ('r2', 'BFL'),
    ('r2', 'NPS'),
    ('P1', 'FFL'),
    ('P2', 'BFL'),
    ('FFL', 'BFL'),
    ('FFL', 'NPS'),
    ('BFL', 'NPS')
]
pairs_failing = [pair for pair in pairs if pair not in pairs_passing]

triplets = combinations(Lens.variables, 3)
# itertools.combinations returns an ordered iterable,
# that is why it is possible to search by the indexes.
# To search by indexes it is needed to make it a list.
# triplets_passing_indexes = 521, 522, 523, 536, 543, 557, 558, 559, 572, 579, 593, 594, 595, 642, 643, 657, 659, 668, 675, 679
# triplets_passing = [triplets[index] for index in triplets_passing_indexes]
triplets_passing = [
    ('r1', 'r2', 'FFL'),
    ('r1', 'r2', 'BFL'),
    ('r1', 'r2', 'NPS'),
    ('r1', 'P1', 'FFL'),
    ('r1', 'P2', 'BFL'),
    ('r1', 'FFL', 'BFL'),
    ('r1', 'FFL', 'NPS'),
    ('r1', 'BFL', 'NPS'),
    ('r2', 'P1', 'FFL'),
    ('r2', 'P2', 'BFL'),
    ('r2', 'FFL', 'BFL'),
    ('r2', 'FFL', 'NPS'),
    ('r2', 'BFL', 'NPS'),
    ('P1', 'FFL', 'BFL'),
    ('P1', 'FFL', 'NPS'),
    ('P2', 'FFL', 'BFL'),
    ('P2', 'BFL', 'NPS'),
    ('f1', 'FFL', 'NPS'),
    ('f2', 'BFL', 'NPS'),
    ('FFL', 'BFL', 'NPS')
]
triplets_failing = [triplet for triplet in triplets if triplet not in triplets_passing]

combinations_passing = chain(
    single_variable_passing,
    pairs_passing,
    triplets_passing
)
combinations_failing = chain(
    single_variable_failing,
    pairs_failing,
    triplets_failing
)


@pytest.mark.parametrize("left_out", combinations_passing)
def test_missing_passing(left_out):
    """
    Check result with combinations missing.
    """
    lens = Lens()
    lens.D1 = 0.00999400000000000
    lens.D2 = 0.0124925000000000
    lens.D = 0.0222367999100000
    lens.n1 = 1.0003
    lens.nL = 1.5
    lens.n2 = 1.0003
    lens.r1 = 50
    lens.r2 = -40
    lens.CT = 3
    lens.P1 = 1.12392500724714
    lens.P2 = -0.899140005797714
    lens.f1 = -44.9839906842963
    lens.f2 = 44.9839906842963
    lens.EFL = 44.9704995344359
    lens.FFL = -43.8600656770491
    lens.BFL = 44.0848506784985
    lens.NPS = 0

    removed = {}
    for variable in left_out:
        removed[variable] = getattr(lens, variable)
        setattr(lens, variable, None)

    lens.calculate()
    for variable in left_out:
        print(variable)
        print(removed[variable])
        print(getattr(lens, variable))
        assert isclose(removed[variable], getattr(lens, variable))


@pytest.mark.parametrize("left_out", combinations_failing)
def test_missing_failing(left_out):
    """
    Test combinations which end up with ValueError.
    """
    lens = Lens()
    lens.D1 = 0.00999400000000000
    lens.D2 = 0.0124925000000000
    lens.D = 0.0222367999100000
    lens.n1 = 1.0003
    lens.nL = 1.5
    lens.n2 = 1.0003
    lens.r1 = 50
    lens.r2 = -40
    lens.CT = 3
    lens.P1 = 1.12392500724714
    lens.P2 = -0.899140005797714
    lens.f1 = -44.9839906842963
    lens.f2 = 44.9839906842963
    lens.EFL = 44.9704995344359
    lens.FFL = -43.8600656770491
    lens.BFL = 44.0848506784985
    lens.NPS = 0

    for variable in left_out:
        setattr(lens, variable, None)

    with pytest.raises(ValueError) as exception_info:
        lens.calculate()
    assert str(exception_info.value) == "SymPy doesn't want to calculate this input!"

