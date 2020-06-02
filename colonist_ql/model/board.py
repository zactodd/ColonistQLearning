import colonist_ql.patterns as patterns


class Board(metaclass=patterns.Singleton):
    def __init__(self, settlement_limit=5, city_limit=5, road_limit=15):
        self.player_dict = None
        self.turn_order = None
        self.hex_dict = None

        self.settlement_limit = settlement_limit
        self.city_limit = city_limit
        self.road_limit = road_limit

    # def __init__(self, players, hexes):
    #     self.player_dict = {p.name: p for p in players}
        # self.hex_dict = {h.cube_coords: h for h in hexes}

    def get_player(self, player_name):
        return self.player_dict[player_name]

    # def setup_game(self, players, hexes):
    #     self.__init__(players, hexes)

    def set_turn_order(self, turn_oder):
        self.turn_order = turn_oder

    def get_hex(self, coord):
        return self.hex_dict[coord]

    def set_hexes(self, hexes):
        if self.hex_dict is None:
            self.hex_dict = {h.cube_coords: h for h in hexes}


# players = {"ZacTodd", "Tami#6966", "Oakes#7878", "bambee"}
# Board([Player(p, "red", players - {p}) for p in players], None)
