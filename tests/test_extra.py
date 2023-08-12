from sympy.core.symbol import Symbol

from lenscalc import Lens


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
