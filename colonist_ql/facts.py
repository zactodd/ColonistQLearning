import functools
import operator
import enum


# Game resources types
class RESOURCES(enum):
    LUMBER = "lumber"
    BRICK = "brick"
    WOOL = "wool"
    GRAIN = "grain"
    ORE = "ore"


# Title
class TILES(RESOURCES):
    DESERT = "desert"
    SEA = "SEA"


PURCHASES = {
    "road": {RESOURCES.LUMBER: 1, RESOURCES.brick: 1},
    "settlement": {RESOURCES.LUMBER: 1, RESOURCES.BRICK: 1, RESOURCES.WOOL: 1, RESOURCES.GRAIN: 1},
    "city": {RESOURCES.GRAIN: 2, RESOURCES.ORE: 3},
    "dev_card": {RESOURCES.WOOL: 1, RESOURCES.GRAIN: 1, RESOURCES.ORE: 1}
}


RESOURCE_COLOURS = {
    "sea": "steelblue",
    "desert": "navajowhite",
    RESOURCES.LUMBER: "forestgreen",
    RESOURCES.WOOL: "lightgreen",
    RESOURCES.GRAIN: "gold",
    RESOURCES.ORE: "slategrey",
    RESOURCES.BRICK: "orange",
}

# Board Information
VALUES = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
HEX_RESOURCES = [RESOURCES.LUMBER, RESOURCES.WOOL, RESOURCES.GRAIN] * 4 + [RESOURCES.BRICK, RESOURCES.ORE] * 3
PORT_FRAMES = [
    [RESOURCES.WOOL, "general"],
    [RESOURCES.LUMBER],
    [RESOURCES.BRICK, "general"],
    ["general"],
    [RESOURCES.BRICK, "general"],
    [RESOURCES.ORE]
]

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

# DICE PIPS
DICE_PIPS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
PREPARED_DICE_DIST = functools.reduce(operator.iconcat, [[k] * v for k, v in DICE_PIPS.items()], [])


