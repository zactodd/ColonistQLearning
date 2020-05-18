import functools
import operator

RESOURCES_TYPES = {"wood", "sheep", "grain", "brick", "ore"}
PURCHASES = {
    "road": {"wood": 1, "brick": 1},
    "settlement": {"wood": 1, "brick": 1, "sheep": 1, "grain": 1},
    "city": {"grain": 2, "ore": 3},
    "dev_card": {"sheep": 1, "grain": 1, "ore": 1}
}


RESOURCE_COLOURS = {
    "sea": "steelblue",
    "desert": "navajowhite",
    "wood": "forestgreen",
    "sheep": "lightgreen",
    "grain": "gold",
    "ore": "slategrey",
    "brick": "orange",
}

# Board Information
VALUES = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
HEX_RESOURCES = ["wood", "sheep", "grain"] * 4 + ["brick", "ore"] * 3
PORT_FRAMES = [["sheep", "general"], ["wood"], ["brick", "general"], ["general"], ["brick", "general"], ["ore"]]

# Build limits
BUILD_LIMITS = {"settlement": 5, "city": 4, "road": 15}

# Development card information.
DEV_CARDS_TYPES = ["vp", "knight", "mono", "yop", "rb"]
DEV_CARDS = 5 * ["vp"] + 14 * ["knight"] + 2 * ["mono", "yop", "rb"]
STARTING_NUM_DEV = len(DEV_CARDS)

PORT_PLACEMENT = {
    # Port format 1
    (-1, 3, -2): (-1, 2, -1),
    (-3, 3, 0): (-2, 2, 0),
    (1, 2, -3): (1, 1, -2),
    (-3, 1, 2): (-2, 1, 1),
    (3, 0, -3): (2, 0, -2),
    (-2, -1, 3): (-1, -1, 2),
    (3, -2, -1): (2, -1, -1),
    (2, -3, 1): (1, -2, 1),
    (-0, -3, 3): (0, -2, 2),

    # Port Format 2
    (-1, -2, 3): (-1, -1, 2),
    (-3, 0, 3): (-2, 0, 2),
    (-3, 2, 1): (-2, 1, 1),
    (-2, 3, -1): (-1, 2, -1),
    (0, 3, -3): (0, 2, -2),
    (2, 1, -3): (1, 1, -2),
    (3, -1, -2): (2, -1, -1),
    (3, -3, 0): (2, -2, 0),
    (1, -3, 2): (1, -2, 1)
}

DICE_PIPS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
PREPARED_DICE_DIST = functools.reduce(operator.iconcat, [[k] * v for k, v in DICE_PIPS.items()], [])

