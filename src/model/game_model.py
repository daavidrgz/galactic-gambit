from entities.living.player.player import Player
from mechanics.magic.magic_level import MagicLevel
from mechanics.technology.gun import Gun
from mechanics.technology.upgrade_system import UpgradeSystem
from systems.rng_system import RngSystem
from utils.singleton import Singleton
import pickle


# TODO: Cuidado con pushear escenas... Al volver de otra escena, hay que tener en cuenta que en la escena
# anterior haya cambiado el modelo y haya que refrescar sprites... si hacemos switch scene no nos afecta
class GameModel(metaclass=Singleton):
    def __init__(self):
        initial_gun = Gun(20, 500, 1, 30, 0.0, 1)
        initial_magic_level = MagicLevel(1, 0)
        initial_player = PlayerModel(100, initial_gun, initial_magic_level)
        self.player = initial_player
        self.level = None
        self.rng_system = RngSystem.get_instance()
        self.upgrade_system = UpgradeSystem.get_instance()

    def __update_model(self, model):
        self.player = model.player
        self.level = model.level
        self.rng_system.set_states(model.rng_system.get_states())
        self.upgrade_system.set_state(
            model.upgrade_system.available_upgrades,
            model.upgrade_system.selected_upgrades,
        )

    def update_player(self, player_sprite: Player):
        self.player = PlayerModel.from_sprite(player_sprite)

    def get_player(self):
        return self.player

    def update_level(self, level):
        self.level = level

    def get_level(self):
        return self.level

    # Serialize with pickle
    def save(self):
        target_file = open("/tmp/save_file", "wb")
        pickle.dump(self, target_file)
        target_file.close()

    # Deserialize with pickle
    def load(self):
        source_file = open("/tmp/save_file", "rb")
        previous_model = pickle.load(source_file)
        source_file.close()
        self.__update_model(previous_model)


class PlayerModel:
    def __init__(self, hp, gun, magic_level):
        self.hp = hp
        self.magic_level = magic_level
        self.gun = gun

    def from_sprite(player_sprite):
        hp = player_sprite.hp
        gun = player_sprite.gun
        magic_level = player_sprite.magic_level
        return PlayerModel(hp, gun, magic_level)
