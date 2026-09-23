"""UNKNOWN Milestone 2.1 visual preview. Run: python visualize_milestone2.py
Keys: 1/2/3 select organism, arrows move, g take energy, Q quit.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

try:
    from organisms.organism import Organism
    from environment.resources import ResourcePatch, ResourceType
    from systems.energy import intake_energy
    from systems.movement import move_organism
    from environment.world import World
except ModuleNotFoundError:
    from UNKNOWN.organisms.organism import Organism # type: ignore
    from UNKNOWN.environment.resources import ResourcePatch, ResourceType # type: ignore
    from UNKNOWN.systems.energy import intake_energy # type: ignore
    from UNKNOWN.systems.movement import move_organism # type: ignore
    from UNKNOWN.environment.world import World # type: ignore

WORLD_WIDTH = 100
WORLD_HEIGHT = 100
BUFFER = 5
INNER_RATIO = 0.60
MAX_INTAKE = 20.0
world = World(WORLD_WIDTH, WORLD_HEIGHT, BUFFER)

usable_w, usable_h = WORLD_WIDTH - 2*BUFFER, WORLD_HEIGHT - 2*BUFFER
inner_w, inner_h = usable_w*INNER_RATIO, usable_h*INNER_RATIO
inner_x, inner_y = (WORLD_WIDTH-inner_w)/2, (WORLD_HEIGHT-inner_h)/2

organisms = [
    Organism(1, (35, 35), 40, 100, 100, 100),
    Organism(2, (65, 60), 75, 100, 100, 100),
    Organism(3, (50, 70), 25, 100, 100, 100),
]
resources = [
    ResourcePatch(ResourceType.ENERGY, 120, (35, 35), 500),
    ResourcePatch(ResourceType.ENERGY, 90, (65, 60), 500),
    ResourcePatch(ResourceType.ENERGY, 160, (50, 70), 500),
]
selected = 0
fig, ax = plt.subplots(figsize=(9, 8))
fig.canvas.manager.set_window_title("UNKNOWN — Milestone 2.1")

def draw():
    ax.clear()
    ax.set(xlim=(0, WORLD_WIDTH), ylim=(0, WORLD_HEIGHT),
           xlabel="X position", ylabel="Y position")
    ax.set_aspect("equal")
    ax.set_xticks(range(0, 101, 10)); ax.set_yticks(range(0, 101, 10))
    ax.grid(True, linewidth=0.35, alpha=0.45)
    # Shaded inaccessible boundary buffer
    for xy, w, h in [((0,0),100,BUFFER), ((0,95),100,BUFFER),
                     ((0,5),BUFFER,90), ((95,5),BUFFER,90)]:
        ax.add_patch(Rectangle(xy,w,h,color="dimgray",alpha=.25))
    ax.add_patch(Rectangle((inner_x,inner_y),inner_w,inner_h,fill=False,
                           edgecolor="royalblue",linewidth=2,linestyle="--",
                           label="Inner living zone"))
    for i,p in enumerate(resources):
        x,y=p.position
        ax.scatter(x,y,marker="s",s=180,color="gold",edgecolors="black",zorder=3)
        ax.annotate(f"R{i+1}: {p.quantity:.0f}",(x,y),xytext=(8,8),
                    textcoords="offset points",fontsize=9)
    for i,o in enumerate(organisms):
        x,y=o.position
        ax.add_patch(Circle((x,y),2.4,facecolor="limegreen",
                            edgecolor=("red" if i==selected else "black"),
                            linewidth=2,zorder=4))
        ax.annotate(f"O{o.organism_id}  E:{o.energy:.0f}",(x,y),
                    xytext=(8,-20),textcoords="offset points",fontsize=9)
    ax.set_title(f"UNKNOWN Milestone 2.1 — O{organisms[selected].organism_id} selected\n"
                 "1/2/3 select • arrows move • g intake energy • Q quit")
    ax.legend(loc="upper right")
    fig.tight_layout(); fig.canvas.draw_idle()

def on_key(event):
    global selected
    if event.key in ("1","2","3"):
        selected=int(event.key)-1
    elif event.key in ("up", "down", "left", "right"):
        o = organisms[selected]
        moved = move_organism(o, world, event.key)
        print(f"O{o.organism_id}: {'moved to ' + str(o.position) if moved else 'movement blocked'}")
    elif event.key and event.key.lower()=="g":
        o,p=organisms[selected],resources[selected]
        gained=intake_energy(o,p,MAX_INTAKE,MAX_INTAKE)
        print(f"O{o.organism_id} gained {gained:.1f}; energy={o.energy:.1f}; resource={p.quantity:.1f}")
    elif event.key and event.key.lower()=="q":
        plt.close(fig)
    draw()

fig.canvas.mpl_connect("key_press_event",on_key)
draw()
print("Preview open: 1/2/3 select, arrow keys move, g take energy, Q quit.")
plt.show()
