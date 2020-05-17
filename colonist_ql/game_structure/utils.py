from colonist_ql.game_structure import cube_coord as cc


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
