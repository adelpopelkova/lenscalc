from math import isclose

import pytest
import sympy

from lenscalc import Lens


def test_setup():
    """
    Test one option how to create a lens.
    """
    lens = Lens(
        n1=1.0003,
        nL=1.5,
        n2=1.0003,
        r1=50,
        r2=-40,
        CT=3
    )

    lens.calculate()

    assert lens.D1 == (lens.nL - lens.n1) / lens.r1
    assert lens.n1 == 1.0003


def test_different_setup():
    """
    Test another option how to create a lens.
    """
    lens = Lens()
    lens.n1 = 1.0003
    lens.nL = 1.5
    lens.n2 = 1.0003
    lens.r1 = 50
    lens.r2 = -40
    lens.CT = 3

    lens.calculate()

    assert lens.D1 == (lens.nL - lens.n1) / lens.r1
    assert lens.n1 == 1.0003


def test_variables_before_calculation():
    """
    Test variables before calculation.
    """
    lens = Lens(
        n1=1.0003,
        nL=1.5,
        n2=1.0003,
        r1=50,
        r2=-40,
        CT=3
    )

    assert lens.n1 == 1.0003
    assert lens.D1 is None


def test_calculated_variables():
    """
    Test if all variables are calculated correctly.
    """
    lens = Lens()
    lens.n1 = 1.0003
    lens.nL = 1.5
    lens.n2 = 1.0003
    lens.r1 = 50
    lens.r2 = -40
    lens.CT = 3

    lens.calculate()

    # math.isclose is used due to the floating point inaccuracy
    assert isclose(lens.D1, (lens.nL - lens.n1) / lens.r1)
    assert isclose(lens.D2, (lens.n2 - lens.nL) / lens.r2)
    assert isclose(lens.D, lens.D1 + lens.D2 - lens.D1 * lens.D2 * (lens.CT / lens.nL))
    assert isclose(lens.P1, (lens.D2 / lens.D) * (lens.n1 / lens.nL) * lens.CT)
    assert isclose(lens.P2, -(lens.D1 / lens.D) * (lens.n2 / lens.nL) * lens.CT)
    assert isclose(lens.f1, -lens.n1 * lens.EFL)
    assert isclose(lens.f2, lens.n2 * lens.EFL)
    assert isclose(lens.EFL, 1 / lens.D)
    assert isclose(lens.FFL, lens.f1 + lens.P1)
    assert isclose(lens.BFL, lens.f2 + lens.P2)
    assert isclose(lens.NPS, lens.f1 + lens.f2)


def test_variables_from_input():
    """
    Test if variables from input aren't overwritten.
    """
    lens = Lens()
    lens.n1 = 1.0003
    lens.nL = 1.5
    lens.n2 = 1.0003
    lens.r1 = 50
    lens.r2 = -40
    lens.CT = 3

    lens.calculate()

    assert lens.n1 == 1.0003
    assert lens.nL == 1.5
    assert lens.n2 == 1.0003
    assert lens.r1 == 50
    assert lens.r2 == -40
    assert lens.CT == 3


def test_calculate_with_all_variables(capsys):
    """
    Test calculation with all variables given.
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
    lens.FFL = 43.8600656770491
    lens.BFL = 44.0848506784985
    lens.NPS = 0

    lens.calculate()

    captured = capsys.readouterr()

    assert "Nothing to compute." in captured.out


@pytest.mark.timeout(120)
def test_calculate_with_no_variables():
    """
    Test calculation with no variables given.
    """
    lens = Lens()

    with pytest.raises(ValueError):
        lens.calculate()


@pytest.mark.timeout(120)  # This test is kind of slow.
def test_not_enough_variables():
    """
    Test input with less variables.
    """
    lens = Lens()
    lens.n1 = 1.0003
    lens.n2 = 1.0003
    lens.r1 = 50
    lens.r2 = -40
    lens.CT = 3

    lens.calculate()

    # At the moment testing only that the result is an expression,
    # currently not testing, that it is the correct expression.
    assert isinstance(lens.D1, sympy.core.expr.Expr)
    assert isinstance(lens.D2, sympy.core.expr.Expr)
    assert isinstance(lens.D, sympy.core.expr.Expr)
    assert isinstance(lens.P1, sympy.core.expr.Expr)
    assert isinstance(lens.P2, sympy.core.expr.Expr)
    assert isinstance(lens.f1, sympy.core.expr.Expr)
    assert isinstance(lens.f2, sympy.core.expr.Expr)
    assert isinstance(lens.EFL, sympy.core.expr.Expr)
    assert isinstance(lens.BFL, sympy.core.expr.Expr)
    assert isinstance(lens.FFL, sympy.core.expr.Expr)
    assert lens.NPS == 0
