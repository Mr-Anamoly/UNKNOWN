"""Energy intake rules for Milestone 2; no automatic feeding or metabolism."""

from organisms.organism import Organism
from environment.resources import ResourcePatch, ResourceType


def intake_energy(
    organism: Organism,
    resource: ResourcePatch,
    requested_amount: float,
    max_intake: float,
) -> float:
    """Transfer energy from a colocated energy patch to an organism.

    Returns the amount gained. Does not move the organism or run automatically.
    """
    if requested_amount < 0 or max_intake < 0:
        raise ValueError("Intake amounts cannot be negative.")
    if not organism.alive:
        return 0.0
    if resource.resource_type != ResourceType.ENERGY:
        return 0.0
    if organism.position != resource.position:
        return 0.0

    room = max(0.0, organism.max_energy - organism.energy)
    amount_to_take = min(requested_amount, max_intake, room, resource.quantity)
    gained = resource.remove(amount_to_take)
    organism.energy += gained
    organism.lifetime_energy_gained += gained
    return gained
