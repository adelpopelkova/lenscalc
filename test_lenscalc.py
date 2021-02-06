from math import isclose

import pytest
import sympy

from lenscalc import Lens


def test_setup():
    """
    Test one option how to create a lens.
    """
    l = Lens(
        n1 = 1.0003,
        nL = 1.5,
        n2 = 1.0003,
        r1 = 50,
        r2 = -40,
        CT = 3
    )

    l.calculate()

    assert l.D1 == (l.nL - l.n1) / l.r1
    assert l.n1 == 1.0003


def test_different_setup():
    """
    Test another option how to create a lens.
    """
    l = Lens()
    l.n1 = 1.0003
    l.nL = 1.5
    l.n2 = 1.0003
    l.r1 = 50
    l.r2 = -40
    l.CT = 3

    l.calculate()

    assert l.D1 == (l.nL - l.n1) / l.r1
    assert l.n1 == 1.0003


def test_variables_before_calculation():
    """
    Test variables before calculation.
    """
    l = Lens(
        n1 = 1.0003,
        nL = 1.5,
        n2 = 1.0003,
        r1 = 50,
        r2 = -40,
        CT = 3
    )

    assert l.n1 == 1.0003
    assert l.D1 is None


def test_calculated_variables():
    """
    Test if all variables are calculated correctly.
    """
    l = Lens()
    l.n1 = 1.0003
    l.nL = 1.5
    l.n2 = 1.0003
    l.r1 = 50
    l.r2 = -40
    l.CT = 3

    l.calculate()

    # math.isclose is used due to the floating point inaccuracy
    assert isclose(l.D1, (l.nL - l.n1) / l.r1)
    assert isclose(l.D2, (l.n2 - l.nL) / l.r2)
    assert isclose(l.D, l.D1 + l.D2 - l.D1 * l.D2 * (l.CT / l.nL))
    assert isclose(l.P1, (l.D2 / l.D) * (l.n1 / l.nL) * l.CT)
    assert isclose(l.P2, -(l.D1 / l.D) * (l.n2 / l.nL) * l.CT)
    assert isclose(l.f1, -l.n1 * l.EFL)
    assert isclose(l.f2, l.n2 * l.EFL)
    assert isclose(l.EFL, 1 / l.D)
    assert isclose(l.FFL, l.f1 + l.P1)
    assert isclose(l.BFL, l.f2 + l.P2)
    assert isclose(l.NPS, l.f1 + l.f2)


def test_variables_from_input():
    """
    Test if variables from input aren't overwritten.
    """
    l = Lens()
    l.n1 = 1.0003
    l.nL = 1.5
    l.n2 = 1.0003
    l.r1 = 50
    l.r2 = -40
    l.CT = 3

    l.calculate()

    assert l.n1 == 1.0003
    assert l.nL == 1.5
    assert l.n2 == 1.0003
    assert l.r1 == 50
    assert l.r2 == -40
    assert l.CT == 3


def test_calculate_with_all_variables(capsys):
    """
    Test calculation with all variables given.
    """
    l = Lens()
    l.D1 = 0.00999400000000000
    l.D2 =  0.0124925000000000
    l.D = 0.0222367999100000
    l.n1 = 1.0003
    l.nL = 1.5
    l.n2 = 1.0003
    l.r1 = 50
    l.r2 = -40
    l.CT = 3
    l.P1 = 1.12392500724714
    l.P2 = -0.899140005797714
    l.f1 = -44.9839906842963
    l.f2 = 44.9839906842963
    l.EFL = 44.9704995344359
    l.FFL = 43.8600656770491
    l.BFL = 44.0848506784985
    l.NPS = 0

    l.calculate()

    captured = capsys.readouterr()

    assert "Nothing to compute." in captured.out


@pytest.mark.skip(reason="Currently gets into an infinite loop.")
@pytest.mark.timeout(120)
def test_calculate_with_no_variables():
    """
    Test calculation with no variables given.

    This test should fail, due to the timeout.
    """
    l = Lens()

    l.calculate()


@pytest.mark.timeout(120)  # This test is kind of slow.
def test_not_enough_variables():
    """
    Test input with less variables.
    """
    l = Lens()
    l.n1 = 1.0003
    l.n2 = 1.0003
    l.r1 = 50
    l.r2 = -40
    l.CT = 3

    l.calculate()

    # At the moment testing only that the result is an expression,
    # currently not testing, that it is the correct expression.
    assert isinstance(l.D1, sympy.core.expr.Expr)
    assert isinstance(l.D2, sympy.core.expr.Expr)
    assert isinstance(l.D, sympy.core.expr.Expr)
    assert isinstance(l.P1, sympy.core.expr.Expr)
    assert isinstance(l.P2, sympy.core.expr.Expr)
    assert isinstance(l.f1, sympy.core.expr.Expr)
    assert isinstance(l.f2, sympy.core.expr.Expr)
    assert isinstance(l.EFL, sympy.core.expr.Expr)
    assert isinstance(l.BFL, sympy.core.expr.Expr)
    assert isinstance(l.FFL, sympy.core.expr.Expr)
    assert isinstance(l.NPS, sympy.core.expr.Expr)

