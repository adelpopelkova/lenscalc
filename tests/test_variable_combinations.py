from copy import deepcopy
from math import isclose

import pytest
from sympy.core.expr import Expr

from lenscalc import Lens
from combinations_for_tests import combinations_passing, combinations_failing

# This lens was compared to the result from the original calculator.
ORIGINAL_LENS = Lens(
    D1=0.00999400000000000,
    D2=0.0124925000000000,
    D=0.0222367999100000,
    n1=1.0003,
    nL=1.5,
    n2=1.0003,
    r1=50,
    r2=-40,
    CT=3,
    P1=1.12392500724714,
    P2=-0.899140005797714,
    f1=-44.9839906842963,
    f2=44.9839906842963,
    EFL=44.9704995344359,
    FFL=-43.8600656770491,
    BFL=44.0848506784985,
    NPS=0
)


def compare_two_lenses(lens1, lens2):
    """
    Compare two lenses.

    Return True if they are the same / close enough.
    Return False if they aren't close enough and print the differences.
    """
    same = True
    for variable in Lens.variables:
        value_lens1 = getattr(lens1, variable)
        value_lens2 = getattr(lens2, variable)
        if isinstance(value_lens1, Lens.numbers) and isinstance(value_lens2, Lens.numbers):
            if not isclose(value_lens1, value_lens2):
                same = False
                print(f"{variable}: {value_lens1}, {value_lens2}")
        else:
            if not (isinstance(value_lens1, Expr) or isinstance(value_lens2, Expr)):
                same = False

    return same


@pytest.mark.parametrize("left_out", combinations_passing)
def test_missing_passing(left_out):
    """
    Check result with combinations missing.
    """
    lens = deepcopy(ORIGINAL_LENS)

    for variable in left_out:
        setattr(lens, variable, None)

    lens.calculate()

    assert compare_two_lenses(ORIGINAL_LENS, lens)


@pytest.mark.parametrize("left_out", combinations_failing)
def test_missing_failing(left_out):
    """
    Test combinations which end up with ValueError.
    """
    lens = deepcopy(ORIGINAL_LENS)

    for variable in left_out:
        setattr(lens, variable, None)

    with pytest.raises(ValueError) as exception_info:
        lens.calculate()

    assert str(exception_info.value).startswith("There has been a problem with the calculation.")
