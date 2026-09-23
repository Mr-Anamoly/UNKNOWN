"""Explicit one-cell organism movement with world-boundary validation."""

DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}


def move_organism(organism, world, direction):
    """Move an organism one cell in a cardinal direction.

    Returns True if movement succeeds, otherwise False. Invalid direction
    names raise ValueError. No energy cost or autonomous decision is applied.
    """
    if not isinstance(direction, str) or direction.lower() not in DIRECTIONS:
        raise ValueError(f"direction must be one of: {', '.join(DIRECTIONS)}")
    if not organism.alive:
        return False

    dx, dy = DIRECTIONS[direction.lower()]
    x, y = organism.position
    destination = (x + dx, y + dy)

    if not world.is_accessible(*destination):
        return False

    organism.position = destination
    return True
