from math import isclose

import pytest

from lenscalc import Lens
from combinations_for_tests import combinations_passing, combinations_failing


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
