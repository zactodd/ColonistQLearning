from colonist_ql.interface_interaction.log_extration.parser import TURN, OPENING, GAME, CLOSING_TURN
from colonist_ql.game_structure.board import Board


def interpret_turn(turn_string):
    turn_dict = TURN.parseString(turn_string).asDict()
    player_turn = Board().get_player(turn_dict["player_turn"])
    for p, r in turn_dict["got_resource"].items():
        Board().get_player(p).add_resources(r[0])


def interpret_opening(opening_string):
    opening_dict = OPENING.parseString(opening_string).asDict()

    for p, r in opening_dict["got_resource"].items():
        Board().get_player(p).add_resources(r[0])
    Board().set_turn_order([p for p, *_ in opening_dict["placement_phase"][0]])



opening = """
bambee turn to place settlement

bambee placed a settlement

bambee turn to place road

bambee placed a road


Tami#6966 turn to place settlement

Tami#6966 placed a settlement

Tami#6966 turn to place road

Tami#6966 placed a road


Oakes#7878 turn to place settlement

Oakes#7878 placed a settlement

Oakes#7878 turn to place road

Oakes#7878 placed a road


ZacTodd turn to place settlement

ZacTodd placed a settlement

ZacTodd turn to place road

ZacTodd placed a road


ZacTodd turn to place settlement

ZacTodd placed a settlement

ZacTodd turn to place road

ZacTodd placed a road


Oakes#7878 turn to place settlement

Oakes#7878 placed a settlement

Oakes#7878 turn to place road

Oakes#7878 placed a road


Tami#6966 turn to place settlement

Bot is placing a settlement for Tami#6966

Tami#6966 placed a settlement

Tami#6966 turn to place road

Tami#6966 placed a road


bambee turn to place settlement

bambee placed a settlement

bambee turn to place road

bambee placed a road


Giving out starting resources

ZacTodd got: lumber grain wool

Tami#6966 got:ore lumber lumber

bambee got: wool wool

Oakes#7878 got: lumber lumber brick
"""

interpret_opening(opening)