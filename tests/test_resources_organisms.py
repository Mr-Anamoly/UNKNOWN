import unittest

from environment.resources import ResourcePatch, ResourceType
from organisms.organism import Organism
from systems.energy import intake_energy


class TestMilestone2(unittest.TestCase):
    def setUp(self):
        self.organism = Organism(
            organism_id=1, position=(10, 10), energy=40, max_energy=100,
            health=100, max_health=100
        )
        self.patch = ResourcePatch(ResourceType.ENERGY, 80, (10, 10), 100)

    def test_intake_transfers_energy(self):
        gained = intake_energy(self.organism, self.patch, 15, 20)
        self.assertEqual(gained, 15)
        self.assertEqual(self.organism.energy, 55)
        self.assertEqual(self.patch.quantity, 65)
        self.assertEqual(self.organism.lifetime_energy_gained, 15)

    def test_intake_respects_organism_capacity(self):
        self.organism.energy = 95
        gained = intake_energy(self.organism, self.patch, 20, 20)
        self.assertEqual(gained, 5)
        self.assertEqual(self.organism.energy, 100)

    def test_intake_respects_patch_quantity(self):
        self.patch.quantity = 3
        gained = intake_energy(self.organism, self.patch, 20, 20)
        self.assertEqual(gained, 3)

    def test_cannot_intake_from_far_away(self):
        self.organism.position = (0, 0)
        self.assertEqual(intake_energy(self.organism, self.patch, 10, 20), 0)

    def test_cannot_intake_non_energy_resource(self):
        nutrient = ResourcePatch(ResourceType.NUTRIENT, 50, (10, 10))
        self.assertEqual(intake_energy(self.organism, nutrient, 10, 20), 0)

    def test_dead_organism_cannot_intake(self):
        self.organism.alive = False
        self.assertEqual(intake_energy(self.organism, self.patch, 10, 20), 0)


if __name__ == "__main__":
    unittest.main()
