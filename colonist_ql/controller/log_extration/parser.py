import ast
import colonist_ql.facts as facts
from pyparsing import *

# Extracts players name.
_PLAYER = Regex(r"(\w)+\d*(\w)*(#\d+)?").setName("player")

# Extracts hex identifier.
_HEX_NUM = Regex(r"\d+").setName("hex_num")

# Extracts hex structure type. i.e. road, settlement or city.
_STRUCTURE = Regex(r"|".join(f"({s.value})" for s in facts.STRUCTURES)).setName("structure")

# Extracts two dice values, and players turn.
_DICE = (Suppress("dice_") + Regex("[1-6]") + Suppress("dice_") + Regex("[1-6]")).setName("dice")
DICE_ROLL = _PLAYER("player_turn") + Suppress("rolled:") + _DICE("dice_rolled")

# Resource types, and who got those resources.
_RESOURCE = Regex(r"|".join(f"({s.value})" for s in facts.RESOURCES)).setName("resource")
_RESOURCES = _RESOURCE * (1,)
GOT_RESOURCES = Dict(Group(_PLAYER + Suppress("got:") + _RESOURCES) * (1, 4))("got_resource")

# Extracts if other victory point conditions.
RECEIVED_LARGEST_ARMY = (
    (_PLAYER + Suppress("received largest army")) |
    (Suppress("largest army has passed from:") + Suppress(_PLAYER) + Suppress("to:") + _PLAYER)
).setName("received_largest_army")
RECEIVED_LONGEST_ROAD = (
        (_PLAYER + Suppress("received longest road")) |
        (Suppress("longest road has passed from:") + Suppress(_PLAYER) + Suppress("to:") + _PLAYER)
).setName("received_longest_road")

# Determines what player is building a what structure.
BOT_STRUCTURE_PLACEMENT = (
        Literal("Bot is placing a") +
        _STRUCTURE +
        Suppress("for") +
        Suppress(_PLAYER)
).setName("bot_placing")
BUILD_STRUCTURE = (
        Suppress(_PLAYER) +
        (Suppress("placed a") | Suppress("built a")) +
        _STRUCTURE("built") +
        RECEIVED_LONGEST_ROAD("received_lr") * (0, 1)
).setName("built_structure")

# Extracts initial turn placement.
PLACEMENT_TURN = (
    _PLAYER +
    Suppress("turn to place") +
    Suppress(_STRUCTURE) +
    Group(BOT_STRUCTURE_PLACEMENT) * (0, 1)
).setName("opening_placement")

# Extracts what resources are proposed in a trade.
PROPOSE_TRADE = Group(
    _PLAYER +
    Suppress("wants to give") +
    Suppress(_PLAYER * (0, 2)) +
    Suppress(":") +
    _RESOURCES("offer") +
    Suppress("for:") +
    _RESOURCES("want")
)("propose_trade").setName("propose_trade")

# Accepted which players accepted a trade.
ACCEPTED_TRADE = Group(_PLAYER + Suppress("traded with:") + _PLAYER)("accepted").setName("accepted_trade")

# Extracts the resource exchange in a bank trade.
BANK_TRADE = Group(
    Suppress(_PLAYER) +
    Suppress("gave bank:") +
    _RESOURCES("gave") +
    Suppress("and took") +
    _RESOURCES("got")
)("bank_trade").setName("propose_trade")

# Determine who is robbing who and what was stolen.
ROBBER_PLACEMENT = Suppress(_PLAYER) + Suppress("moved robber") + Suppress("to tile:") + _HEX_NUM("moved_to")
PERSONAL_ROBBING = Suppress("You stole:") + _RESOURCE("gain_resource") + Suppress("from:") + Suppress(_PLAYER)
STOLE_CARD = _PLAYER("player_robbing") + Suppress("stole card from:") + _PLAYER("player_stolen")
ROBBER_ACTION = Group(ROBBER_PLACEMENT + STOLE_CARD + PERSONAL_ROBBING * (0, 1))("robbing_info")

# Extracts what player is purchasing a dev card.
PURCHASED_DEV_CARD = Suppress(_PLAYER) + Suppress("bought") + Literal("development card")

# Development usage and type.
_CARD = Regex(r"(knight)|(monopoly)|(road building)|(year of plenty)").setName("dev_card")
CARD_USE = Suppress(_PLAYER) + Suppress("used") + _CARD("type")

# Card usage.
PLAYED_KNIGHT = CARD_USE + RECEIVED_LARGEST_ARMY("received_la") * (0, 1) + ROBBER_ACTION
PLAYED_MONO = CARD_USE + Suppress("& stole all of:") + _RESOURCE("got")
PLAYED_RB = CARD_USE + BUILD_STRUCTURE * 2
PLAYED_YOP = CARD_USE + Suppress(_PLAYER) + Suppress("took from bank:") + (_RESOURCE * 2)("got")


# Exracts which dev card was played.
PLAYED_CARD = Group(PLAYED_KNIGHT | PLAYED_MONO | PLAYED_RB | PLAYED_YOP)("played_dev_card")

# Determines what how many cards are being discarded by players and what cards are discarded.
_TO_DISCARD = Dict(Group(
    _PLAYER +
    Suppress("has:") +
    Regex(r"\d+")("hand_amount") +
    Suppress("card.") +
    Suppress("Needs to discard:") +
    Regex(r"\d+")("num_cards_remove") +
    Suppress("card")
) * (1, 4))("to_discard")
DISCARD = Dict(Group(_PLAYER + Suppress("discarded:") + _RESOURCES) * (1, 4))("discarded")

# Actiosn that occures that are not playing a dev card.
_NON_DEV_CARD_ACTION = (
    Group(PURCHASED_DEV_CARD) |
    Group(PROPOSE_TRADE) |
    Group(BANK_TRADE) |
    Group(ACCEPTED_TRADE) |
    Group(BUILD_STRUCTURE)
)

# Disconnections and reconnection.
DISCONNECTION = (
    _PLAYER +
    Suppress("has disconnected, a bot will continue the game. Bot will wait a little to give") +
    Suppress(_PLAYER) +
    Suppress("a chance to join back")
)
RECONNECTION = (
    Suppress("Karma System: Active again. You will receive a karma penalty if you leave the game") +
    _PLAYER +
    Suppress("has reconnected!")
)
CONNECTION = DISCONNECTION | RECONNECTION

_DICE_PHASE = (
        (DICE_ROLL + GOT_RESOURCES) |
        (DICE_ROLL + Suppress(_TO_DISCARD) + DISCARD + ROBBER_ACTION) |
        DICE_ROLL
)
TURN = (
    (
            PLAYED_CARD +
            _DICE_PHASE +
            (_NON_DEV_CARD_ACTION * (0, ))("actions")
    ) |
    (
            _DICE_PHASE +
            (_NON_DEV_CARD_ACTION * (0, ))("actions") +
            PLAYED_CARD * (0, 1) +
            (_NON_DEV_CARD_ACTION * (0, ))("actions")
    )
)
ORBIT = TURN * 4

OPENING_PLACEMENT_TURN = Group(
    PLACEMENT_TURN +
    Suppress(
        BUILD_STRUCTURE +
        PLACEMENT_TURN +
        BUILD_STRUCTURE
    )
)
OPENING_PLACEMENT_ORBIT = Group(OPENING_PLACEMENT_TURN * 4)
OPENING_RESOURCE_ALLOCATION = Suppress("Giving out starting resources") + GOT_RESOURCES
OPENING = (OPENING_PLACEMENT_ORBIT * 2)("placement_phase") + OPENING_RESOURCE_ALLOCATION

CLOSING_STATEMENT = Suppress("trophy") + _PLAYER("winner") + Suppress("won the game! trophy")
CLOSING_TURN = (
    (CARD_USE + CLOSING_STATEMENT) |
    (_DICE_PHASE + CARD_USE + CLOSING_STATEMENT) |
    CLOSING_STATEMENT
)


GAME = (
    Suppress(
        "Disable chat with \"/disablechat\" /help for more commands\n\n" +
        "Type \"/help\" for more commands\n\n" +
        "Karma System: Active. Leavers will receive a karma penalty"
    ) +
    OPENING("Opening") +
    (
        Group(TURN) * (1, ) +
        Group(CLOSING_TURN)
    )("turns")
)
