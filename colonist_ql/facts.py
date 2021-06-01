import functools
import operator
import colonist_ql.game_images as game_images
import os
from enum import Enum


# Game resources types
class RESOURCES(Enum):
    LUMBER = "lumber"
    BRICK = "brick"
    WOOL = "wool"
    GRAIN = "grain"
    ORE = "ore"


# Title types
class TILES(Enum):
    LUMBER = "lumber"
    BRICK = "brick"
    WOOL = "wool"
    GRAIN = "grain"
    ORE = "ore"
    DESERT = "desert"
    SEA = "sea"


# Structures types
class STRUCTURES(Enum):
    ROAD = "road"
    SETTLEMENT = "settlement"
    CITY = "city"


# Purchasable types
class PURCHASABLE(Enum):
    ROAD = "road"
    SETTLEMENT = "settlement"
    CITY = "city"
    DEV_CARD = "dev_card"


# Dev cards
class DEV_CARD:
    VP = "vp"
    KNIGHT = "knight"
    MONO = "monopoly"
    YOP = "year of plenty"
    RB = "road building"


PURCHASES = {
    PURCHASABLE.ROAD: {RESOURCES.LUMBER: 1, RESOURCES.BRICK: 1},
    PURCHASABLE.SETTLEMENT: {RESOURCES.LUMBER: 1, RESOURCES.BRICK: 1, RESOURCES.WOOL: 1, RESOURCES.GRAIN: 1},
    PURCHASABLE.CITY: {RESOURCES.GRAIN: 2, RESOURCES.ORE: 3},
    PURCHASABLE.DEV_CARD: {RESOURCES.WOOL: 1, RESOURCES.GRAIN: 1, RESOURCES.ORE: 1}
}

RESOURCE_COLOURS = {
    TILES.SEA: "steelblue",
    TILES.DESERT: "navajowhite",
    RESOURCES.LUMBER: "forestgreen",
    RESOURCES.WOOL: "lightgreen",
    RESOURCES.GRAIN: "gold",
    RESOURCES.ORE: "slategrey",
    RESOURCES.BRICK: "orange",
    TILES.LUMBER: "forestgreen",
    TILES.WOOL: "lightgreen",
    TILES.GRAIN: "gold",
    TILES.ORE: "slategrey",
    TILES.BRICK: "orange"
}

# Board Information
DICE_VALUES = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
HEX_RESOURCES = [TILES.LUMBER, TILES.WOOL, TILES.GRAIN] * 4 + [TILES.BRICK, TILES.ORE] * 3 + [TILES.DESERT]
PORT_FRAMES = [
    [RESOURCES.WOOL, "general"],
    [RESOURCES.LUMBER],
    [RESOURCES.BRICK, "general"],
    ["general"],
    [RESOURCES.BRICK, "general"],
    [RESOURCES.ORE]
]

# Build limits
BUILD_LIMITS = {STRUCTURES.SETTLEMENT: 5, STRUCTURES.CITY: 4, STRUCTURES.ROAD: 15}

# Development card information.
DEV_CARDS = 5 * [DEV_CARD.VP] + 14 * [DEV_CARD.KNIGHT] + 2 * [DEV_CARD.MONO, DEV_CARD.YOP, DEV_CARD.RB]
STARTING_NUM_DEV = len(DEV_CARDS)


PORT_FRAMES_0 = {
    (-1, 3, -2): (-1, 2, -1),
    (-3, 3, 0): (-2, 2, 0),
    (1, 2, -3): (1, 1, -2),
    (-3, 1, 2): (-2, 1, 1),
    (3, 0, -3): (2, 0, -2),
    (-2, -1, 3): (-1, -1, 2),
    (3, -2, -1): (2, -1, -1),
    (2, -3, 1): (1, -2, 1),
    (-0, -3, 3): (0, -2, 2),
}


PORT_FRAMES_1 = {
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

# Game Images directories
GAME_IMAGE_DIR = list(game_images.__path__)[0]

PORT_IMAGE_DIR = f"{GAME_IMAGE_DIR}/icons"
SETTLEMENT_IMAGES_DIR = f"{GAME_IMAGE_DIR}/settlements"
CITY_IMAGES_DIR = f"{GAME_IMAGE_DIR}/cities"
ROAD_IMAGES_DIR = f"{GAME_IMAGE_DIR}/road"
