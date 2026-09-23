import unittest

from environment.world import World
from organisms.organism import Organism
from systems.movement import move_organism


class TestMovement(unittest.TestCase):
    def setUp(self):
        self.world = World(width=20, height=20, boundary_buffer=2)
        self.organism = Organism(
            organism_id=1, position=(10, 10), energy=50, max_energy=100,
            health=100, max_health=100
        )

    def test_moves_one_cell_in_each_cardinal_direction(self):
        for direction, expected in [
            ("up", (10, 9)), ("down", (10, 11)),
            ("left", (9, 10)), ("right", (11, 10)),
        ]:
            self.organism.position = (10, 10)
            self.assertTrue(move_organism(self.organism, self.world, direction))
            self.assertEqual(self.organism.position, expected)

    def test_cannot_enter_boundary_buffer(self):
        self.organism.position = (2, 10)
        self.assertFalse(move_organism(self.organism, self.world, "left"))
        self.assertEqual(self.organism.position, (2, 10))

    def test_cannot_leave_world(self):
        self.organism.position = (19, 10)
        self.assertFalse(move_organism(self.organism, self.world, "right"))
        self.assertEqual(self.organism.position, (19, 10))

    def test_dead_organism_cannot_move(self):
        self.organism.alive = False
        self.assertFalse(move_organism(self.organism, self.world, "up"))
        self.assertEqual(self.organism.position, (10, 10))

    def test_invalid_direction_raises_value_error(self):
        with self.assertRaises(ValueError):
            move_organism(self.organism, self.world, "diagonal")

    def test_direction_is_case_insensitive(self):
        self.assertTrue(move_organism(self.organism, self.world, "UP"))
        self.assertEqual(self.organism.position, (10, 9))


if __name__ == "__main__":
    unittest.main()
