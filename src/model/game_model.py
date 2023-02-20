from model.player_model import PlayerModel
from utils.singleton import Singleton


class GameModel(metaclass=Singleton):
    def __init__(self):
        self.player = None
        self.level = None

    def set_player(self, player):
        self.player = player
