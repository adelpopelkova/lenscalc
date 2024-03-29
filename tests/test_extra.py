from copy import copy, deepcopy

from sympy.core.symbol import Symbol

from lenscalc import Lens
from test_variable_combinations import compare_two_lenses, ORIGINAL_LENS


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


def test_extra_string():
    """
    Test lens with extra attributes of string type.

    The attributes should not be converted to type float.
    """
    lens = Lens()

    lens.extra_string_text = "extra"
    lens.extra_string_number = "1.5"

    assert isinstance(lens.extra_string_text, str)
    assert isinstance(lens.extra_string_number, str)


def test_copy():
    """
    Test that it is posible to create a copy of a lens.

    The copied lens is a unique object.
    """
    lens = copy(ORIGINAL_LENS)

    assert lens is not ORIGINAL_LENS
    assert compare_two_lenses(ORIGINAL_LENS, lens)

    setattr(lens, "NPS", None)
    assert lens.NPS != ORIGINAL_LENS.NPS


def test_deepcopy():
    """
    Test that it is posible to create a deep copy of a lens.
    """
    lens = deepcopy(ORIGINAL_LENS)

    assert lens is not ORIGINAL_LENS
    assert compare_two_lenses(ORIGINAL_LENS, lens)

    setattr(lens, "NPS", None)
    assert lens.NPS != ORIGINAL_LENS.NPS


def test_copy_extra():
    """
    Test copy of a lens with an extra attribute.
    """
    lens1 = Lens()
    lens1.extra = "extra"

    lens2 = copy(lens1)

    assert lens1 is not lens2
    assert lens1.extra == lens2.extra
