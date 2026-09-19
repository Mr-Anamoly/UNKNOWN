"""Static classification of cells into inner, outer, and buffer zones."""
from config import INNER_ZONE_RATIO
from .world import CellType


class ZoneMap:
    """Builds a centered rectangular inner zone within a World."""

    def __init__(self, world, inner_zone_ratio=INNER_ZONE_RATIO):
        if inner_zone_ratio is None:
            raise ValueError("INNER_ZONE_RATIO is not configured in config.py.")
        if (isinstance(inner_zone_ratio, bool)
                or not isinstance(inner_zone_ratio, (int, float))
                or not 0 < inner_zone_ratio <= 1):
            raise ValueError("inner_zone_ratio must be greater than 0 and <= 1.")

        self.world = world
        self.inner_zone_ratio = float(inner_zone_ratio)

        usable_width = world.width - 2 * world.boundary_buffer
        usable_height = world.height - 2 * world.boundary_buffer
        self.inner_width = max(1, int(usable_width * self.inner_zone_ratio))
        self.inner_height = max(1, int(usable_height * self.inner_zone_ratio))

        # Center the rectangle within the accessible area.
        self.inner_x_min = (world.width - self.inner_width) // 2
        self.inner_y_min = (world.height - self.inner_height) // 2
        self.inner_x_max = self.inner_x_min + self.inner_width  # exclusive
        self.inner_y_max = self.inner_y_min + self.inner_height  # exclusive

        # Ensure rounding never pushes the inner zone into the buffer.
        b = world.boundary_buffer
        if (self.inner_x_min < b or self.inner_y_min < b
                or self.inner_x_max > world.width - b
                or self.inner_y_max > world.height - b):
            raise ValueError("Inner zone does not fit inside accessible area.")

    def classify(self, x, y):
        """Return CellType; raise IndexError for coordinates outside world."""
        if not self.world.is_in_bounds(x, y):
            raise IndexError(f"Coordinate {(x, y)} is outside the world.")
        if self.world.is_buffer_cell(x, y):
            return CellType.BUFFER
        if (self.inner_x_min <= x < self.inner_x_max
                and self.inner_y_min <= y < self.inner_y_max):
            return CellType.INNER
        return CellType.OUTER

    def is_inner(self, x, y):
        return self.classify(x, y) == CellType.INNER

    def is_outer(self, x, y):
        return self.classify(x, y) == CellType.OUTER

    def is_buffer(self, x, y):
        return self.classify(x, y) == CellType.BUFFER
