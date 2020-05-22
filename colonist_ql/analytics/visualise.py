from colonist_ql.analytics.analytics import *
from colonist_ql.game_structure.board import Board
from colonist_ql.game_structure.structures import *
import colonist_ql.facts as facts
import colonist_ql.game_structure.cube_coord as cc
import scipy.stats as stats
import matplotlib.pyplot as plt


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
    :param include_blocked: If to count block titles.
    :param density: If True shows the per roll expectation based on the rolls otherwise show the total.
    """
    resources, counts = resources_from_settlements(settlements, rolls, include_blocked, density)
    plt.bar(resources, counts)
    plt.show()


def plot_expected_resources_from_settlements(settlements, include_blocked=False):
    """
    PLot the expected resources per turn given a collection of settlements.
    :param settlements: The settlements that resources can be obtained.
    :param include_blocked: If to count block titles.
    """
    plot_resource_from_settlements(settlements, dice_distribution(10000), include_blocked, True)


def current_settlement_resources_expectation(include_blocked=False):
    """
    PLot the expected resources per turn given a the current board position.
    :param include_blocked: If to count block titles.
    """
    plot_expected_resources_from_settlements(Settlements.get_all(), include_blocked)


def plot_maximum_expected_resources():
    """
    PLot the expected resources per turn given if a settlement was built on every triple point.
    """
    settlements = [Settlement(t, dummy=True) for t in cc.triples_from_centre(3)]
    plot_expected_resources_from_settlements(settlements, False)


def plot_player_bank_rates(player):
    """
    Plot the bank rate of the player.
    :param player:
    """
    resources, rate = player.bank_rates.items()
    plt.bar(resources, rate)
    plt.show()
