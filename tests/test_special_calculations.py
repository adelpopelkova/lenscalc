from math import isclose

from sympy import oo  # infinity in SymPy
from sympy.core.symbol import Symbol

from lenscalc import Lens
from test_variable_combinations import compare_two_lenses


def test_different_refractive_index():
    """
    Test calculation of a lens with different refractive indexes.

    And check that NPS isn't 0.
    """
    lens = Lens(
        n1=1.0003,  # air
        nL=1.5,
        n2=1.33,  # water
        r1=50,
        r2=-40,
        CT=3
    )

    lens.calculate()

    # This lens was compared to the result from the original calculator.
    assert isclose(lens.D1, 0.00999400000000000)
    assert isclose(lens.D2, 0.00425000000000000)
    assert isclose(lens.D, 0.0141590510000000)
    assert isclose(lens.n1, 1.0003)
    assert isclose(lens.nL, 1.5)
    assert isclose(lens.n2, 1.33)
    assert isclose(lens.r1, 50)
    assert isclose(lens.r2, -40)
    assert isclose(lens.CT, 3)
    assert isclose(lens.P1, 0.600502816184503)
    assert isclose(lens.P2, -1.87752978642425)
    assert isclose(lens.f1, -70.6473901393533)
    assert isclose(lens.f2, 93.9328490306307)
    assert isclose(lens.EFL, 70.6262022786697)
    assert isclose(lens.FFL, -70.0468873231688)
    assert isclose(lens.BFL, 92.0553192442064)
    assert isclose(lens.NPS, 23.2854588912774)

    assert lens.NPS != 0


def test_extra_symbol():
    """
    Test lens with an extra attribute of Symbol type.
    """
    lens = Lens()

    extra = Symbol("extra")

    # Set the arttribute.
    lens.extra = extra
    # Try to get the value of the attribute.
    extra_attribute = lens.extra

    assert extra_attribute == extra


def test_planar_surface_lens():
    """
    Test a lens with one surface as infinity.
    """
    lens = Lens(
        n1=1.0003,
        nL=1.5,
        n2=1.0003,
        r1=oo,
        r2=-40,
        CT=3
    )

    lens.calculate()

    # This lens was compared to the result from the original calculator.
    comparison_lens = Lens(
        D1=0,
        D2=0.0124925000000000,
        D=0.0124925000000000,
        n1=1.0003,
        nL=1.5,
        n2=1.0003,
        r1=oo,
        r2=-40,
        CT=3,
        P1=2.00060000000000,
        P2=0,
        f1=-80.0720432259355,
        f2=80.0720432259355,
        EFL=80.0480288172904,
        FFL=-78.0714432259355,
        BFL=80.0720432259355,
        NPS=0
    )

    assert compare_two_lenses(comparison_lens, lens)
