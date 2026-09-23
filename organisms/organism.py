"""Basic organism data. Behavior such as movement is added in later milestones."""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Organism:
    organism_id: int
    position: Tuple[int, int]
    energy: float
    max_energy: float
    health: float
    max_health: float
    age: int = 0
    lifetime_energy_gained: float = 0.0
    lifetime_energy_spent: float = 0.0
    alive: bool = True

    def __post_init__(self):
        if self.max_energy < 0 or self.max_health < 0:
            raise ValueError("Maximum energy and health cannot be negative.")
        self.energy = min(max(self.energy, 0.0), self.max_energy)
        self.health = min(max(self.health, 0.0), self.max_health)
        if self.health == 0:
            self.alive = False
