from abc import ABC, abstractmethod
from colonist_ql.game_structure import cube_coord as cc
import colonist_ql.patterns as patterns
import colonist_ql.facts as facts


class Road:
    def __init__(self, edge, dummy=False):
        self.edge = edge
        self.planner_coords = cc.edge_planer_position(edge)

        if not dummy:
            Roads().add()


class Settlement:
    def __init__(self, triple, is_city=False, dummy=False):
        self.triple = triple
        self.is_city = is_city
        self.port = self._port(triple)

        if not dummy:
            Settlements().add(self)

    @staticmethod
    def _port(triple):
        p = Ports()
        return p.get(triple) if p.has(triple) else None

    def upgrade(self):
        self.is_city = True

    def has_port(self):
        return self.port is not None


class Port:
    def __init__(self, sea_coord, land_cord, text, dummy=False):
        self.sea_coord = sea_coord
        self.land_coord = land_cord
        self.edge = (sea_coord, land_cord)
        self.triples = tuple(frozenset({sea_coord, land_cord, t}) for t in cc.triples_from_neighbours(*self.edge))
        self.transfer_rates = self._transfer_rates(text)

        if not dummy:
            Ports().add(self)

    @staticmethod
    def _transfer_rates(text):
        if "3:1" in text:
            return {p: 3 for p in facts.RESOURCES_TYPES}
        elif "2:1" in text:
            for r in facts.RESOURCES_TYPES:
                if r in text:
                    return {r: 2}
        raise Exception("Port text is not in a valid format.")

    def get_rates(self):
        return self.transfer_rates


class Structures(metaclass=patterns.PolymorphicSingleton):
    def __init__(self):
        self.structures_dict = {}

    @abstractmethod
    def add(self, item):
        """
        Adds a structure to the structures
        :param item: The item to add.
        """
        NotImplementedError()

    def has(self, item):
        return item in self.structures_dict

    def get(self, key):
        return self.structures_dict[key]

    def get_all(self):
        return self.structures_dict.values()


class Ports(Structures):
    def __init__(self):
        super().__init__()

    def add(self, port):
        """
        Adds a port to the ports.
        :param port: The port to be added.
        """
        if not self.has(port):
            t1, t2 = port.triples
            self.structures_dict[t1] = port
            self.structures_dict[t2] = port


class Settlements(Structures):
    def __init__(self):
        super().__init__()

    def add(self, settlement):
        """
        Adds a settlement to the settlements.
        :param settlement: The settlement to be added.
        """
        self.structures_dict[settlement.triple] = settlement


class Roads(Structures):
    def __init__(self):
        super().__init__()

    def add(self, road):
        """
        Adds a road to the settlements.
        :param road: The road to be added.
        """
        self.structures_dict[road.edge] = road


def road_options(owned_roads, placed_roads):
    """
    Gets all the possible placement options for additional roads.
    :param owned_roads: The roads you own.
    :param placed_roads: The roads placed in the game.
    :return: A set of placement edges.
    """
    return {potential for r in owned_roads for potential in cc.edge_neighbours(r) if potential not in placed_roads}


def house_options(owned_roads, placed_house):
    """
    Gets all the possible placement options for additional houses.
    :param owned_roads: The roads you own.
    :param placed_house: The houses placed in the game.
    :return: A set of placement vertices.
    """
    restricted = set()
    for h in placed_house:
        restricted.add(cc.triple_neighbours(h))
    return {
        potential for r in owned_roads for potential in cc.triples_from_neighbours(*r) if potential not in restricted
    }
