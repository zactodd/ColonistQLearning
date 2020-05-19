from abc import ABC, abstractmethod
from colonist_ql.game_structure import cube_coord as cc
import colonist_ql.patterns as patterns
import colonist_ql.facts as facts
from collections import defaultdict


class Hex:
    def __init__(self, cube_coords, real_coords, resource, value, blocked=False):
        self.cube_coords = cube_coords
        self.real_coords = real_coords
        self.resource = resource
        self.value = value
        self.edges = {frozenset({cube_coords, n}) for n in cc.neighbours(cube_coords)}
        self.vertices = cc.triples(cube_coords)
        self.blocked = blocked


class Road:
    def __init__(self, edge, dummy=False):
        self.edge = edge
        self.planner_coords = cc.edge_planer_position(edge)

        if not dummy:
            Roads().add(self)

    def __str__(self):
        t1, t2 = cc.triples_from_neighbours(*self.edge)
        return f"Road between {string_triple(t1)} and {string_triple(t2)}."


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

    def __str__(self):
        type_str = "City" if self.is_city else "Settlement"
        return f"{type_str} on {string_triple(self.triple)}"


class Port:
    def __init__(self, sea_coord, land_cord, text, dummy=False):
        self.sea_coord = sea_coord
        self.land_coord = land_cord
        self.edge = (sea_coord, land_cord)
        self.triples = tuple(frozenset({sea_coord, land_cord, t}) for t in cc.triples_from_neighbours(*self.edge))
        self.transfer_rates = self._transfer_rates(text)
        self.text = text

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

    def __str__(self):
        port_text = " ".join(self.text.split("\n"))
        t1, t2 = self.triples
        return f"Port trading {port_text} on {string_triple(t1)} and {string_triple(t2)}."


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


class Hexes(Structures):
    def __init__(self):
        super().__init__()

    def add(self, h):
        """
        Adds a hex to the hexes.
        :param h: The hex to be added.
        """
        self.structures_dict[h.cube_coords] = h


class Ports(Structures):
    def __init__(self):
        super().__init__()

    def add(self, port):
        """
        Adds a port to the ports.
        :param port: The port to be added.
        """
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
    restricted_edges = {r.edge for r in placed_roads}
    return {potential for r in owned_roads for potential in cc.edge_neighbours(r.edges)} - restricted_edges


def potential_settlement_triples(owned_roads, placed_settlements=None):
    """
    Gets all the possible placement options for additional settlements.
    :param owned_roads: The roads that are owned by the player.
    :param placed_settlements: The houses settlements in the game.
    :return: A set of placement triples.
    """
    if placed_settlements is None:
        placed_settlements = Settlements().get_all()
    restricted = _restricted_settlement_placements(placed_settlements)
    return {potential for r in owned_roads for potential in cc.triples_from_neighbours(*r.edge)} - restricted


def potential_settlement_upgrades(owned_settlements):
    """
    Gets all the possible options for upgrading settlements.
    :param owned_settlements: The settlements that are owned by the player.
    :return: A set of settlement that can be upgraded.
    """
    return {s for s in owned_settlements if not s.is_city}


def _restricted_settlement_placements(placed_settlements):
    return {t for s in placed_settlements for t in {s.triple} | cc.triple_neighbours(s.triple)}


def placement_phase_settlement_triples(placed_settlements=None):
    """
    Gets all the possible placement options for settlements in the placement phase.
    :param placed_settlements: The houses settlements in the game.
    :return: A set of placement triples.
    """
    if placed_settlements is None:
        placed_settlements = Settlements().get_all()
    return cc.triples_from_centre(2) - _restricted_settlement_placements(placed_settlements)


def longest_road(owned_roads):
    """
    Calculates the length of the longest road.
    :param owned_roads: The roads that are owned by the player.
    :return: An int representing the length of the road.
    """
    road_dict = {r.edge: r for r in owned_roads}
    graph = {e: [n for n in cc.edge_neighbours(e) if n in road_dict] for e, r in road_dict.items()}
    return len(max(_dfs(graph)))


def _dfs(graph, vertex=None, seen=None, path=None):
    if seen is None:
        seen = []
    paths = []
    if vertex is None:
        for i in graph:
            paths.extend(_dfs(graph, i, seen[:], [i]))
    else:
        if path is None:
            path = [vertex]
        seen.append(vertex)
        for t in graph[vertex]:
            if t not in seen:
                t_path = path + [t]
                paths.append(tuple(t_path))
                paths.extend(_dfs(graph, t, seen[:], t_path))
    return paths


def string_hex(h):
    """
    Coverts a hex to a single letter repressing it general purpose.
    :param h: The hex to represented.
    :return: A string of len 1.
    """
    value = h.value
    if value is None:
        return "D" if h.resource == "desert" else "S"
    elif isinstance(value, int):
        return str(value)
    else:
        return "P"


def string_triple(t, coord_format="readable"):
    """
    Converts a triple to a string.
    :param t: The triple to be converted.
    :param coord_format: The format in which the triple will be displayed.
    :return: A string representing the triple.
    """
    assert coord_format in ["readable", "cube", "axial"], \
        f"The coord_format {coord_format} is not valid, uses either readable, cube or axial."
    if coord_format == "readable":
        if any(not Hexes().has(c) for c in t):
            return string_triple(t, "cube")
        else:
            return " ".join(string_hex(Hexes().get(c)) for c in cc.planer_order(t))
    elif coord_format == "axial":
        return " ".join(cc.cube_to_axial(c) for c in cc.planer_order(t))
    else:
        return " ".join(cc.planer_order(t))
