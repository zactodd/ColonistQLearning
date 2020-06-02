import numpy as np
from collections import defaultdict, Counter
from colonist_ql.model.structures import *


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


def resources_max_expected(inland_scaling=1, coast_scaling=1):
    rolls = dice_distribution(10000)
    settlements = [Settlement(t, dummy=True) for t in cc.triples_from_centre(3)]
    if inland_scaling == coast_scaling == 1:
        return resources_from_settlements(settlements, rolls, False, True)
    else:
        rolls_dict = defaultdict(Counter)
        coastal_ring = cc.ring_from_centre(3)
        for s in settlements:
            is_coastal = any(c in coastal_ring for c in s.triple)
            scaling = coast_scaling if is_coastal else inland_scaling
            for c in s.triple:
                h = Hexes().get(c)
                rolls_dict[h.value][h.resource] += 1 * scaling
        recourse_obtained = Counter()
        for roll in rolls:
            for res, i in rolls_dict[roll].items():
                recourse_obtained[res] += i
        resources, counts = recourse_obtained.keys(), recourse_obtained.values()
        counts = [c / len(rolls) for c in counts]
        return resources, counts


def i2c3():
    """
    Calculates max expect resources with inland settlement being calculated at 1/2 and coastal settlements at 1/3.
    :return: resources and the there count per roll.
    """
    return resources_max_expected(1 / 2, 1 / 3)


def i3c5():
    """
    Calculates max expect resources with inland settlement being calculated at 1/3 and coastal settlements at 1/3.
    :return: resources and the there count per roll.
    """
    return resources_max_expected(1 / 3, 1 / 5)
