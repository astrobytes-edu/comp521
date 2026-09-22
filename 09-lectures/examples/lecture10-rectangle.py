"""Lecture 10: validated state and a computed property."""
from math import isfinite
from numbers import Real


def positive_dimension(value):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError('dimension must be a positive finite real number')
    try:
        dimension = float(value)
    except OverflowError as exc:
        raise ValueError('dimension must be a positive finite real number') from exc
    if not isfinite(dimension) or dimension <= 0:
        raise ValueError('dimension must be a positive finite real number')
    return dimension


class Rectangle:
    def __init__(self, width, height):
        self._width = positive_dimension(width)
        self._height = positive_dimension(height)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def area(self):
        return self.width * self.height


rect = Rectangle(3, 4)
assert rect.area == 12
