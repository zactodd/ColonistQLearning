import colonist_ql.facts as facts
import colonist_ql.game_structure.structures as structures
from colonist_ql.game_structure.board import Board
from collections import Counter


class Player:
    def __init__(self, name, colour, opponents, settlements=None, roads=None, dev_cards=None, hand=None, knights=0,
                 has_longest_road=False, has_largest_army=False):
        self.name = name
        self.colour = colour
        self.opponents = opponents

        self.settlements = settlements if settlements is not None else []
        self.num_cities, self.num_settlements = self._update_settlement_count()

        self.roads = roads if roads is not None else []
        self.road_length = self._calculate_road_length()

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
        rates = {r: 4 for r in facts.facts.RESOURCES}
        if len(ports) == 0:
            return rates
        for p in ports:
            for i, r in p.get_rates().items():
                if rates[i] > r:
                    rates[i] = r
        return rates

    def _update_settlement_count(self):
        num_cities, num_settlement = 0, 0
        for s in self.settlements:
            num_cities if s.is_city else num_settlement += 1
        return num_cities, num_settlement

    def _update_vp(self):
        self._update_has_largest_army()
        self._update_longest_road()
        self.vp = self.calculate_vp()

    def _update_rates(self, rates):
        for r, i in rates.items():
            if self.bank_rates[i] > r:
                self.bank_rates = r

    def _calculate_road_length(self):
        if len(self.roads) == 0:
            return 0
        else:
            return structures.longest_road(self.roads)

    def _can_purchase(self, price):
        return all(self.hand[r] > c for r, c in price.items())

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

    def _update_longest_road(self):
        if not self.has_largest_army:
            self.has_longest_road = len(self.roads) >= 3 and \
                                    all(o.road_length < self.road_length for o in self.opponents)

    def _update_has_largest_army(self):
        if not self.has_largest_army:
            self.has_largest_army = self.knights >= 3 and all(o.knights < self.knights for o in self.opponents)
            for o in self.opponents:
                o.has_largest_army = False

    def add_knight(self):
        self.knights += 1
        self._update_has_largest_army()

    def purchase_options(self):
        options = []
        for r, c in self.hand.items():
            rate = self.bank_rates[r]
            if rate <= c:
                options.extend([({r: rate}, {i: 1}) for i in facts.facts.RESOURCES - {r}])
        for i, req in facts.PURCHASES.items():
            if all(self.hand[r] > c for r, c in req.items()):
                options.append((req, i))
        return options

    def add_settlement(self, settlement):
        self.settlements.append(settlement)
        self._update_vp()
        self._update_settlement_count()

    def upgrade_settlement(self, settlement):
        for s in self.settlements:
            if s == settlement:
                settlement.upgrade()
        self._update_vp()
        self._update_settlement_count()

    def add_road(self, road):
        """
        Adds road to the player.
        :param road: THe road to be added.
        """
        self.roads.append(road)
        self._calculate_road_length()
        self._calculate_road_length()

    def potential_settlements_locations(self):
        """
        Determines potential settlement locations.
        :return: A set of triples representing the settlement locations.
        """
        return structures.potential_settlement_triples(self.roads)

    def potential_road_locations(self):
        """
        Determines potential edge locations.
        :return: A set of edges representing the road locations.
        """
        return structures.potential_road_edges(self.roads)

    def potential_city_locations(self):
        """
        Determines potential city locations.
        :return: A set of triples representing the city locations.
        """
        return structures.potential_settlement_upgrades(self.settlements)

    def can_place_settlement(self):
        """
        Determines if a settlement can be placed.
        :return: True if a settlement can be place otherwise False.
        """
        return self.num_settlements < Board().settlement_limit and \
               self._can_purchase(facts.PURCHASES["settlement"]) and \
               len(self.potential_settlements_locations()) > 0

    def can_place_city(self):
        """
        Determines if a city can be placed.
        :return: True if a city can be place otherwise False.
        """
        return self.num_cities < Board().settlement_limit and \
               self._can_purchase(facts.PURCHASES["city"]) and \
               len(self.potential_city_locations()) > 0

    def can_place_road(self):
        """
        Determines if a road can be placed.
        :return: True if a road can be place otherwise False.
        """
        return len(self.roads) < Board().road_limit and \
               self._can_purchase(facts.PURCHASES["road"]) and \
               len(self.potential_road_locations()) > 0

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

    def __dict__(self):
        return {
            "name": self.name,
            "colour": self.colour,
            "vp": self.vp
        }

    def __str__(self):
        resources_string = "\n".join(f"\t{r:<8}: {c:02}" for r, c in self.hand.items())
        return f"{self.colour} Player {self.name}:\n" \
               f"Score: {self.vp}\n" \
               f"\tSettlements VP: {self.settlement_vp()}\n" \
               f"\tHas Longest Road: {self.has_largest_army}\n" \
               f"\tHas Largest Army: {self.has_largest_army}\n" \
               f"\tKnights: {self.knights}\n" \
               f"Resources:\n {resources_string}"
