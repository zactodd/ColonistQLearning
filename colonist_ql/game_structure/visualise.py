import matplotlib.pyplot as plt
from colonist_ql import facts
from colonist_ql.game_structure import cube_coord as cc
from colonist_ql.game_structure import structures
from matplotlib.patches import RegularPolygon
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np


def value_colours(value):
    if value in (6, 8):
        return "red"
    else:
        return "black"


def draw_coords(hexes, coord_format="cube"):
    """
    Draws the coords of the triple.
    :param hexes: A collection of Hex objects.
    :param coord_format: The coord format.
    """
    assert coord_format in ["cube", "axial"], f"The coord_format {coord_format} is not valid, uses either cube or axial."

    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor("white")
    ax.set_aspect("equal")
    for h in hexes:

        x, y = cc.planer_position(h.cube_coords)
        patch = RegularPolygon((x, y), numVertices=6, facecolor="white", radius=2 / 3, orientation=0, edgecolor="k")
        ax.add_patch(patch)

        if coord_format == "cube":
            q, r, s = h.cube_coords
            q, r, s = int(q), int(r), int(s)
            if (q, r, s) == (0, 0, 0):
                q, r, s, = "x", "z", "y"
            ax.text(x - 1 / 3 + 0.05, y + 2 / 9 - 0.04, q, color="red", ha="center", va="center", size=16)
            ax.text(x + 1 / 3 - 0.05, y + 2 / 9 - 0.04, r, color="blue", ha="center", va="center", size=16)
            ax.text(x, y - 4 / 9 + 0.12, s, color="green", ha="center", va="center", size=16)
        elif coord_format == "axial":
            q, r = cc.cube_to_axial(h.cube_coords)
            q, r = int(q), int(r)
            if (q, r) == (0, 0):
                q, r = "q", "r"
            ax.text(x - 1 / 3 + 0.05, y, q, color="dodgerblue", ha="center", va="center", size=18)
            ax.text(x + 1 / 3 - 0.05, y, r, color="limegreen", ha="center", va="center", size=18)

    ax.scatter(0, 0, alpha=0.0)
    ax.axis("off")
    plt.show()


def draw_board(hexes, draw_ports=True):
    """
    Draws the board using hex and port information.
    :param hexes: A collection of Hex objects.
    :param ports: A collection of Port objects
    """
    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor(facts.RESOURCE_COLOURS["sea"])
    ax.set_aspect("equal")
    for h in hexes:
        x, y = cc.planer_position(h.cube_coords)
        colour = facts.RESOURCE_COLOURS[h.resource]
        label = h.value
        label_colour = value_colours(h.value)

        patch = RegularPolygon((x, y), numVertices=6, facecolor=colour, radius=2 / 3, orientation=0, edgecolor="k")
        ax.add_patch(patch)
        if ":" in str(label):
            size = 10 if "2:1" in label else 15
        else:
            size = 20
        ax.text(x, y, label, color=label_colour, ha="center", va="center", size=size)

    if draw_ports:
        _draw_ports()

    # oi = OffsetImage(plt.imread("../../game_images/settlement_red.png"), zoom=0.02)
    # ab = AnnotationBbox(oi, (0.667, 0.0), frameon=False)
    # ax.add_artist(ab)
    _draw_roads(cc.all_edges_from_centre(3), "red")
    ax.axis("off")

    # ax.scatter(0, 0, alpha=0.0)
    plt.show()


def _draw_ports():
    """
    Draws in the ports on the map.
    """
    for p in structures.Ports().get_all():
        sx, sy = cc.planer_position(p.sea_coord)
        (ax, ay), (bx, by) = (cc.triple_planner_position(t) for t in p.triples)

        sax, say, sbx, sby = (sx + ax) / 2, (sy + ay) / 2, (sx + bx) / 2, (sy + by) / 2

        plt.plot([ax, sax], [ay, say], c="brown", linewidth=3)
        plt.plot([bx, sbx], [by, sby], c="brown", linewidth=3)


def _draw_roads(roads, colour):
    for r in roads:
        h, v = list(zip(*cc.edge_planer_position(r)))
        plt.plot(h, v, c=colour, linewidth=5)


def _draw_settlements(settlement, colours):
    h_positions = []
    v_positions = []
    for s in settlement:
        h, v = zip(*cc.triple_planner_position(s.triple))
        h_positions.append(np.mean(h))
        v_positions.append(np.mean(v))
    plt.scatter(h_positions, v_positions, c="b", marker="h", s=400, zorder=10, alpha=0.7)
