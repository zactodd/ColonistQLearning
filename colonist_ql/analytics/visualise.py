from colonist_ql.analytics.analytics import *
from colonist_ql.model.board import Board
from colonist_ql.model.structures import *
import colonist_ql.facts as facts
import colonist_ql.model.cube_coord as cc
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib import cm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def plot_dice_rolls(rolls):
    """
    Plots the dice rolls against the expected dice roll curve.
    :param rolls: THe roils to plot.
    """
    rolls_hist, _ = np.histogram(rolls, bins=11)
    dd_hist, _ = np.histogram(facts.PREPARED_DICE_DIST, bins=11)
    scaled_hist = dd_hist / np.size(facts.PREPARED_DICE_DIST) * len(rolls)

    threshold_x = []
    threshold_y = []
    for i, y in enumerate(scaled_hist, 2):
        threshold_x.extend([i - 0.5, i + 0.5])
        threshold_y.extend([y, y])

    plt.bar(range(2, 13), rolls_hist, alpha=0.5)
    plt.plot(threshold_x, threshold_y, "k--")
    plt.show()


def plot_resource_from_settlements(settlements, rolls, include_blocked=False, density=False):
    """
    PLots the resources gain from the.
    :param settlements: An iterable of settlements.
    :param rolls: An iterable of rolls.
    :param include_blocked: If to count block TILES.
    :param density: If True shows the per roll expectation based on the rolls otherwise show the total.
    """
    resources, counts = resources_from_settlements(settlements, rolls, include_blocked, density)
    plt.bar(resources, counts)
    plt.show()


def plot_expected_resources_from_settlements(settlements, include_blocked=False):
    """
    PLot the expected resources per turn given a collection of settlements.
    :param settlements: The settlements that resources can be obtained.
    :param include_blocked: If to count block TILES.
    """
    plot_resource_from_settlements(settlements, dice_distribution(10000), include_blocked, True)


def current_settlement_resources_expectation(include_blocked=False):
    """
    PLot the expected resources per turn given a the current board position.
    :param include_blocked: If to count block TILES.
    """
    plot_expected_resources_from_settlements(Settlements.get_all(), include_blocked)


def plot_maximum_expected_resources():
    """
    PLot the expected resources per turn given if a settlement was built on every triple point.
    """
    resources, counts = resources_max_expected()
    plt.bar(resources, counts)
    plt.show()


def plot_player_bank_rates(player):
    """
    Plot the bank rate of the player.
    :param player:
    """
    resources, rate = player.bank_rates.items()
    plt.bar(resources, rate)
    plt.show()


def plot_expected_i2c3():
    """
    PLot expected resources for using i2c3 metric.
    """
    resources, counts = i2c3()
    plt.bar(resources, counts)
    plt.show()


def plot_expected_i3c5():
    """
    PLot expected resources for using i3c5 metric.
    """
    resources, counts = i3c5()
    plt.bar(resources, counts)
    plt.show()


def plot_triples_heatmap(n_colours=13):
    """
    Plots the heatmap of all of the triples.
    """
    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor(facts.RESOURCE_COLOURS[facts.TILES.SEA])
    ax.set_aspect("equal")

    colours = cm.get_cmap("PuRd", n_colours)
    for t in cc.triples_from_centre(3):
        s = 0
        for c in t:
            h = Hexes().get(c)
            if isinstance(h.value, int):
                s += facts.DICE_PIPS[h.value]
        x, y = cc.triple_planner_position(t)
        plt.scatter(x, y, c=[colours(s)], s=1.6 ** (13 * (s / n_colours)), zorder=10, alpha=0.8)

    _draw_hexes(Hexes().get_all(), ax)
    _draw_ports()

    ax.axis("off")
    plt.show()


def plot_triples_diversity_heatmap(n_colours=13):
    """
    Plots the heatmap of all of the triples take diversity.
    """
    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor(facts.RESOURCE_COLOURS[facts.TILES.SEA])
    ax.set_aspect("equal")
    colours = cm.get_cmap("PuRd", n_colours)

    resources_counters = Counter()
    triples_pips = defaultdict(Counter)
    triples = cc.triples_from_centre(3)
    been_counted = set()
    for t in triples:
        for c in t:
            h = Hexes().get(c)
            if isinstance(h.value, int):
                pips = facts.DICE_PIPS[h.value]
                if h not in been_counted:
                    resources_counters[h.resource] += pips
                    been_counted.add(h)
                triples_pips[t][h.resource] += pips

    for t, resource_pips in triples_pips.items():
        s = int(sum(p / resources_counters[r] for r, p in resource_pips.items()) * (n_colours - 1))
        x, y = cc.triple_planner_position(t)
        plt.scatter(x, y, c=[colours(s)], s=1.6 ** (13 * (s / n_colours)), zorder=10, alpha=0.8)

    _draw_hexes(Hexes().get_all(), ax)
    _draw_ports()

    ax.axis("off")
    # ax.scatter(0, 0, alpha=0.0)
    plt.show()


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

    format_dict = {
        "cube": _draw_coords_cube_format,
        "axial": _draw_coords_spiral_format,
        "spiral": _draw_coords_spiral_format,
        "rows": _draw_coords_cube_format_rows
    }
    assert coord_format in format_dict, \
        f"The coord_format {coord_format} is not valid, uses one of " + ", ".join(format_dict.keys()) + "."

    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor("white")
    ax.set_aspect("equal")

    format_dict[coord_format](hexes, ax)

    ax.scatter(0, 0, alpha=0.0)
    ax.axis("off")
    plt.show()


def _draw_coords_cube_format(hexes, ax):
    for h in hexes:

        x, y = cc.planer_position(h.cube_coords)
        patch = RegularPolygon((x, y), numVertices=6, facecolor="white", radius=2 / 3, orientation=0, edgecolor="k")
        ax.add_patch(patch)

        q, r, s = h.cube_coords
        q, r, s = int(q), int(r), int(s)
        if (q, r, s) == (0, 0, 0):
            q, r, s, = "x", "z", "y"
        ax.text(x - 1 / 3 + 0.05, y + 2 / 9 - 0.04, q, color="red", ha="center", va="center", size=16)
        ax.text(x + 1 / 3 - 0.05, y + 2 / 9 - 0.04, r, color="blue", ha="center", va="center", size=16)
        ax.text(x, y - 4 / 9 + 0.12, s, color="green", ha="center", va="center", size=16)


def _draw_coords_axial_format(hexes, ax):
    for h in hexes:
        x, y = cc.planer_position(h.cube_coords)
        patch = RegularPolygon((x, y), numVertices=6, facecolor="white", radius=2 / 3, orientation=0, edgecolor="k")
        ax.add_patch(patch)

        q, r = cc.cube_to_axial(h.cube_coords)
        q, r = int(q), int(r)
        if (q, r) == (0, 0):
            q, r = "q", "r"
        ax.text(x - 1 / 3 + 0.05, y, q, color="dodgerblue", ha="center", va="center", size=18)
        ax.text(x + 1 / 3 - 0.05, y, r, color="limegreen", ha="center", va="center", size=18)


def _draw_coords_spiral_format(hexes, ax):
    for i, c in enumerate(cc.spiral_order([h.cube_coords for h in hexes]), start=1):
        x, y = cc.planer_position(c)
        patch = RegularPolygon((x, y), numVertices=6, facecolor="white", radius=2 / 3, orientation=0, edgecolor="k")
        ax.add_patch(patch)

        if i == len(hexes):
            i = "x"
        ax.text(x, y, i, color="black", ha="center", va="center", size=20)


def _draw_coords_cube_format_rows(hexes, ax):
    for i, c in enumerate(cc.rows_order([h.cube_coords for h in hexes]), start=1):
        x, y = cc.planer_position(c)
        patch = RegularPolygon((x, y), numVertices=6, facecolor="white", radius=2 / 3, orientation=0, edgecolor="k")
        ax.add_patch(patch)

        if i == np.ceil(len(hexes) / 2):
            i = "x"
        ax.text(x, y, i, color="black", ha="center", va="center", size=20)


def draw_board(hexes, draw_ports=True):
    """
    Draws the board using hex and port information.
    :param hexes: A collection of Hex objects.
    :param draw_ports: A collection of Port objects
    """
    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor(facts.RESOURCE_COLOURS[facts.TILES.SEA])
    ax.set_aspect("equal")
    _draw_hexes(hexes, ax)

    if draw_ports:
        _draw_ports()

    # oi = OffsetImage(plt.imread("../../game_images/settlement_red.png"), zoom=0.02)
    # ab = AnnotationBbox(oi, (0.667, 0.0), frameon=False)
    # ax.add_artist(ab)
    # _draw_roads(cc.all_edges_from_centre(3), "red")
    ax.axis("off")

    ax.scatter(0, 0, alpha=0.0)
    plt.show()


def _draw_hexes(hexes, ax):
    for h in hexes:
        x, y = cc.planer_position(h.cube_coords)
        colour = facts.RESOURCE_COLOURS[h.resource]
        label = h.value
        label_colour = value_colours(h.value)

        patch = RegularPolygon((x, y), numVertices=6, facecolor=colour, radius=2 / 3, orientation=0, edgecolor="k")
        ax.add_patch(patch)
        if ":" in str(label):
            size = 8 if "2:1" in label else 15
        else:
            size = 20
        ax.text(x, y, label, color=label_colour, ha="center", va="center", size=size)


def _draw_ports():
    """
    Draws in the ports on the map.
    """
    for p in Ports().get_all():
        sx, sy = cc.planer_position(p.sea_coord)
        (ax, ay), (bx, by) = (cc.triple_planner_position(t) for t in p.triples)

        sax, say, sbx, sby = (sx + ax) / 2, (sy + ay) / 2, (sx + bx) / 2, (sy + by) / 2

        plt.plot([ax, sax], [ay, say], c="brown", linewidth=3)
        plt.plot([bx, sbx], [by, sby], c="brown", linewidth=3)


def _draw_roads(roads, colour):
    for r in roads:
        h, v = list(zip(*cc.edge_planer_position(r)))
        plt.plot(h, v, c=colour, linewidth=5)


def _draw_settlements(colours_triples, ax):
    for c, v in colours_triples.items():
        for t in v:
            x, y = cc.triple_planner_position(t)
            image = plt.imread(f"{facts.SETTLEMENT_IMAGES_DIR}/settlement_{c}.png")
            oi = OffsetImage(image, zoom=0.15)
            ab = AnnotationBbox(oi, (x, y), frameon=False)
            ax.add_artist(ab)
