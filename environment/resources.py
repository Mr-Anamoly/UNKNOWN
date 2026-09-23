"""Simple resource patches that store a limited amount of material."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class ResourceType(Enum):
    ENERGY = "energy"
    NUTRIENT = "nutrient"
    DEFENSIVE_MATERIAL = "defensive_material"


@dataclass
class ResourcePatch:
    resource_type: ResourceType
    quantity: float
    position: Tuple[int, int]
    max_quantity: Optional[float] = None

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Resource quantity cannot be negative.")
        if self.max_quantity is not None:
            if self.max_quantity < 0:
                raise ValueError("Maximum quantity cannot be negative.")
            self.quantity = min(self.quantity, self.max_quantity)

    def remove(self, amount: float) -> float:
        """Remove up to amount and return how much was actually removed."""
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        taken = min(amount, self.quantity)
        self.quantity -= taken
        return taken
