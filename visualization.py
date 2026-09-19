"""Optional static environment visualization. Requires matplotlib."""
from environment import CellType


def plot_environment(world, zones, show_grid=True):
    """Display the configured static grid; does not advance or simulate state."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from matplotlib.patches import Patch

    # Numeric map: 0=buffer, 1=outer, 2=inner
    values = {
        CellType.BUFFER: 0,
        CellType.OUTER: 1,
        CellType.INNER: 2,
    }
    grid = [
        [values[zones.classify(x, y)] for x in range(world.width)]
        for y in range(world.height)
    ]

    cmap = ListedColormap(["#333333", "#e8c878", "#76b7a5"])
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(grid, origin="upper", cmap=cmap, vmin=0, vmax=2,
              interpolation="nearest")
    ax.set_title("UNKNOWN — Static Environment")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    if show_grid and world.width <= 150 and world.height <= 150:
        ax.set_xticks(range(world.width), minor=True)
        ax.set_yticks(range(world.height), minor=True)
        ax.grid(which="minor", linewidth=0.2, alpha=0.35)
    ax.legend(handles=[
        Patch(color="#76b7a5", label="Inner living zone"),
        Patch(color="#e8c878", label="Outer ring"),
        Patch(color="#333333", label="Boundary buffer (inaccessible)"),
    ], loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=1)
    fig.tight_layout()
    plt.show()
