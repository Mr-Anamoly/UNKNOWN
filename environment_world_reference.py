"""Static bounded grid. This module tells the structure."""
from enum import Enum
from config import WORLD_WIDTH, WORLD_HEIGHT, BOUNDARY_BUFFER


class CellType(str, Enum):
    INNER = "inner"
    OUTER = "outer"
    BUFFER = "buffer"


class World:
    """Stores grid dimensions and provides safe coordinate utilities."""

    def __init__(self, width=WORLD_WIDTH, height=WORLD_HEIGHT,
                 boundary_buffer=BOUNDARY_BUFFER):
        self.width = self._positive_int(width, "width")
        self.height = self._positive_int(height, "height")
        self.boundary_buffer = self._nonnegative_int(
            boundary_buffer, "boundary_buffer"
        )

        if self.width <= 2 * self.boundary_buffer:
            raise ValueError("width must exceed twice the boundary buffer.")
        if self.height <= 2 * self.boundary_buffer:
            raise ValueError("height must exceed twice the boundary buffer.")

    @staticmethod
    def _positive_int(value, name):
        if value is None:
            raise ValueError(f"{name} is not configured in config.py.")
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")
        return value

    @staticmethod
    def _nonnegative_int(value, name):
        if value is None:
            raise ValueError(f"{name} is not configured in config.py.")
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer.")
        return value

    def is_in_bounds(self, x, y):
        """True if coordinate is inside the full grid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_buffer_cell(self, x, y):
        """True for the inaccessible outermost buffer cells."""
        if not self.is_in_bounds(x, y):
            return False
        b = self.boundary_buffer
        return x < b or y < b or x >= self.width - b or y >= self.height - b

    def is_accessible(self, x, y):
        """True for in-bounds cells outside the boundary buffer."""
        return self.is_in_bounds(x, y) and not self.is_buffer_cell(x, y)

    def iter_coordinates(self):
        """Yield every coordinate as (x, y), row by row."""
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y)
