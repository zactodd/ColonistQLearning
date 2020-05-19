from abc import ABC, abstractmethod
from colonist_ql.game_structure import cube_coord as cc
import colonist_ql.patterns as patterns
import colonist_ql.facts as facts
from collections import defaultdict


class Road:
    def __init__(self, edge, dummy=False):
        self.edge = edge
        self.planner_coords = cc.edge_planer_position(edge)

        if not dummy:
            Roads().add(self)


class Settlement:
    def __init__(self, triple, is_city=False, port=None, dummy=False):
        self.triple = triple
        self.is_city = is_city
        self.port = self._port(triple) if port is None else port

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


def potential_road_edges(owned_roads, placed_roads=None):
    """
    Gets all the possible placement options for additional roads.
    :param owned_roads: The roads that are owned by the player.
    :param placed_roads: roads that have ready been place, by default gets roads in the Roads singleton
    :return: A set of placement edges.
    """
    if placed_roads is None:
        placed_roads = Roads().get_all()
    edges = {r.edge for r in placed_roads}
    return {potential for r in owned_roads for potential in cc.edge_neighbours(r.edges) if potential not in edges}


def potential_settlement_triples(owned_roads, placed_settlements=None):
    """
    Gets all the possible placement options for additional settlements.
    :param owned_roads: The roads that are owned by the player.
    :param placed_settlements: The houses settlements in the game.
    :return: A set of placement triples.
    """
    if placed_settlements is None:
        placed_settlements = Settlements().get_all()
    restricted = {t for h in placed_settlements for t in cc.triple_neighbours(h.triple)}
    return {
        potential for r in owned_roads for potential in cc.triples_from_neighbours(*r.edge)
        if potential not in restricted
    }


def potential_settlement_upgrades(owned_settlements):
    """
    Gets all the possible options for upgrading settlements.
    :param owned_settlements: The settlements that are owned by the player.
    :return: A set of settlement that can be upgraded.
    """
    return {s for s in owned_settlements if not s.is_city}


def longest_road(owned_roads):
    road_dict = {r.edge: r for r in owned_roads}
    graph = {e: [n for n in cc.edge_neighbours(e) if n in road_dict] for e, r in road_dict.items()}
    return len(max(_dfs(graph)))


def _dfs(graph, v=None, seen=None, path=None):
    if seen is None:
        seen = []
    if path is None:
        path = [v]
    seen.append(v)

    paths = []
    if v is None:
        for i in graph:
            paths.extend(_dfs(graph, i, seen[:], [i]))
    else:
        for t in graph[v]:
            if t not in seen:
                t_path = path + [t]
                paths.append(tuple(t_path))
                paths.extend(_dfs(graph, t, seen[:], t_path))
    return paths
