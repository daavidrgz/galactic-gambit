class GameModel:
    _instance = None

    def get_instance():
        if GameModel._instance is None:
            GameModel._instance = GameModel()
        return GameModel._instance
