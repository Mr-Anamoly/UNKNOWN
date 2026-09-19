"""Basic geometry tests. Run after filling config.py values."""
import unittest
from environment.world import World, CellType
from environment.zones import ZoneMap


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.world = World(width=100, height=100, boundary_buffer=5)
        self.zones = ZoneMap(self.world, inner_zone_ratio=0.60)

    def test_world_dimensions(self):
        self.assertEqual((self.world.width, self.world.height), (100, 100))

    def test_buffer_is_inaccessible(self):
        self.assertFalse(self.world.is_accessible(0, 50))
        self.assertTrue(self.world.is_accessible(5, 5))
        self.assertTrue(self.world.is_accessible(5, 50))
        self.assertTrue(self.world.is_accessible(94, 94))
        self.assertFalse(self.world.is_accessible(95, 50))

    def test_zone_classification(self):
        self.assertEqual(self.zones.classify(50, 50), CellType.INNER)
        self.assertEqual(self.zones.classify(10, 10), CellType.OUTER)
        self.assertEqual(self.zones.classify(2, 2), CellType.BUFFER)

    def test_out_of_bounds_raises(self):
        with self.assertRaises(IndexError):
            self.zones.classify(100, 100)


if __name__ == "__main__":
    unittest.main()
