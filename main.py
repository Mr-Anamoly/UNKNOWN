"""Create and display the static UNKNOWN environment."""
from config import SHOW_GRID_LINES
from environment import World, ZoneMap
from visualization import plot_environment


def main():
    world = World()
    zones = ZoneMap(world)
    print(f"World: {world.width} x {world.height}")
    print(f"Inner zone: {zones.inner_width} x {zones.inner_height}")
    print(f"Boundary buffer: {world.boundary_buffer} cells")
    plot_environment(world, zones, show_grid=SHOW_GRID_LINES)


if __name__ == "__main__":
    main()
