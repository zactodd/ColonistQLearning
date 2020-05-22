import numpy as np
from collections import defaultdict, Counter
from colonist_ql.game_structure.structures import *


def dice_distribution(size):
    return np.random.randint(1, 7, size) + np.random.randint(1, 7, size)


def resources_from_settlements(settlements, rolls, include_blocked=False, density=False):
    rolls_dict = defaultdict(Counter)
    for s in settlements:
        for c in s.triple:
            if not include_blocked or not c.is_blocked:
                h = Hexes().get(c)
                rolls_dict[h.value][h.resource] += 1 + s.is_city
    recourse_obtained = Counter()
    for roll in rolls:
        for res, i in rolls_dict[roll].items():
            recourse_obtained[res] += i
    resources, counts = recourse_obtained.keys(), recourse_obtained.values()
    if density:
        counts = [c / len(rolls) for c in counts]
    return resources, counts
