import colonist_ql.patterns as patterns
import colonist_ql.interface_interaction.feature_extration as fe
from colonist_ql.game_structure.board import Board


class ExtractorHandler(metaclass=patterns.Singleton):
    def __init__(self):
        self.extractors = {}
        self.add_extractor("InitialBoard", InitialBoardExtractor)
        self.add_extractor("LogExtractor", InitialBoardExtractor)

    def add_extractor(self, key, class_reference):
        self.extractors[key] = class_reference

    def get_extraction(self, key, **kwargs):
        return self.extractors[key](**kwargs)


class Extractor:
    def __init__(self):
        pass

    def extract(self):
        NotImplementedError()


class LogExtractor(Extractor):
    def __init__(self, log_position):

        self.log_position = log_position

    def extract(self):
        NotImplementedError()


class InitialBoardExtractor(Extractor):
    def __init__(self, game_image):
        self.game_image = game_image

    def extract(self):
        hexes = fe.initial_board_extraction(self.game_image)
        Board().set_hexes(hexes)
