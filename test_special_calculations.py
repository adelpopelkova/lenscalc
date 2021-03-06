from math import isclose

from lenscalc import Lens


def test_different_refractive_index():
    """
    Test calculation of a lens with different refractive indexes.

    And check that NPS isn't 0.
    """
    lens = Lens(
        n1 = 1.0003,  # air
        nL = 1.5,
        n2 = 1.33,  # water
        r1 = 50,
        r2 = -40,
        CT = 3
    )

    lens.calculate()

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
