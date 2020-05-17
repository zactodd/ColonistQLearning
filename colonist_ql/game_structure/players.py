import colonist_ql.game_structure.utils as utils
import colonist_ql.facts as facts
from collections import Counter


class Player:
    def __init__(self, name, colour, opponents, settlements=None, roads=None, dev_cards=None, hand=None, knights=0,
                 has_longest_road=False, has_largest_army=False):
        self.name = name
        self.colour = colour
        self.opponents = opponents

        self.settlements = settlements if settlements is not None else []
        self.roads = roads if roads is not None else []

        self.hand = hand if hand is not None else Counter()

        self.dev_cards = dev_cards if dev_cards is not None else []
        self.knights = knights

        self.ports = self._init_ports(self.settlements)
        self.bank_rates = self._init_bank_rate(self.ports)

        self.has_longest_road = has_longest_road
        self.has_largest_army = has_largest_army

        self.vp = self.calculate_vp()

    @staticmethod
    def _init_ports(settlements):
        return {h.port for h in settlements if h.has_port()}

    @staticmethod
    def _init_bank_rate(ports):
        rates = {r: 4 for r in facts.RESOURCES_TYPES}
        if len(ports) == 0:
            return rates
        for p in ports:
            for i, r in p.get_rates().items():
                if rates[i] > r:
                    rates[i] = r
        return rates

    def _update_vp(self):
        self.does_now_has_largest_army()
        self.does_now_has_longest_road()
        self.vp = self.calculate_vp()

    def _update_rates(self, rates):
        for r, i in rates.items():
            if self.bank_rates[i] > r:
                self.bank_rates = r

    def settlement_vp(self):
        return sum(1 + s.is_city for s in self.settlements)

    def calculate_vp(self):
        """
        Calculates a players VP
        :return:
        """
        cards_vp = self.dev_cards.count("vp")
        threshold_vp = 2 * (self.has_largest_army + self.has_longest_road)
        return self.settlement_vp() + cards_vp + threshold_vp

    def does_now_has_longest_road(self):
        # TODO implement
        return self.has_longest_road

    def does_now_has_largest_army(self):
        if self.has_largest_army:
            return True
        elif self.knights >= 3:
            return all(self.knights > o.knights for o in self.opponents)
        else:
            return False

    def add_knight(self):
        self.knights += 1
        self.has_largest_army = self.does_now_has_largest_army()

    def purchase_options(self):
        options = []
        for r, c in self.hand.items():
            rate = self.bank_rates[r]
            if rate <= c:
                options.extend([({r: rate}, {i: 1}) for i in facts.RESOURCES_TYPES - {r}])
        for i, req in facts.PURCHASES.items():
            if all(self.hand[r] > c for r, c in req.items()):
                options.append((req, i))
        return options

    def add_settlement(self, settlement):
        self.settlements.append(settlement)
        self._update_vp()

    def upgrade_settlement(self, settlement):
        for s in self.settlements:
            if s == settlement:
                settlement.upgrade()
        self._update_vp()

    def draw_cards(self, cards):
        for c in cards:
            self.hand[c] += 1

    def play_dev_card(self, dev_card):
        # TODO implement other cases
        if dev_card == "knight":
            self.knights += 1
            self._update_vp()

    def add_resources(self, *resource):
        """
        Adds resources in to players hand.
        :param resource: The resources to be added.
        """
        for r in resource:
            self.hand[r] += 1








