from colonist_ql.game_structure import cube_coord as cc


class Hex:
    def __init__(self, cube_coords, real_coords, resource, value, blocked=False):
        self.cube_coords = cube_coords
        self.real_coords = real_coords
        self.resource = resource
        self.value = value
        self.edges = {frozenset({cube_coords, n}) for n in cc.neighbours(cube_coords)}
        self.vertices = cc.triples(cube_coords)
        self.blocked = blocked
