from model.player_model import PlayerModel


class GameModel:
    _instance = None

    def get_instance():
        if GameModel._instance is None:
            GameModel._instance = GameModel()
        return GameModel._instance

    def __init__(self):
        self.player = None
        self.level = None

    def set_player(self, player):
        self.player = player
