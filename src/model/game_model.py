from constants.game_constants import (
    INITIAL_GUN_COOLDOWN,
    INITIAL_GUN_DAMAGE,
    INITIAL_GUN_N_BULLETS,
    INITIAL_GUN_OFFSET,
    INITIAL_GUN_SPEED,
    INITIAL_GUN_SPREAD,
)
from entities.living.hp import Hp
from entities.living.player.player import Player
from mechanics.magic.magic_level import MagicLevel
from mechanics.gun import Gun
from mechanics.magic.magic_upgrade_system import MagicUpgradeSystem
from mechanics.technology.tech_upgrade_system import TechUpgradeSystem
from systems.rng_system import RngSystem
from utils.singleton import Singleton
import pickle
import os


# TODO: Cuidado con pushear escenas... Al volver de otra escena, hay que tener en cuenta que en la escena
# anterior haya cambiado el modelo y haya que refrescar sprites... si hacemos switch scene no nos afecta

SAVE_FILE_NAME = "savegame_ciie"


class GameModel(metaclass=Singleton):
    def __init__(self):
        # TODO: Guardar esto aquí o en constants?

        initial_gun = Gun(
            INITIAL_GUN_DAMAGE,
            INITIAL_GUN_COOLDOWN,
            INITIAL_GUN_SPEED,
            INITIAL_GUN_OFFSET,
            INITIAL_GUN_SPREAD,
            INITIAL_GUN_N_BULLETS,
        )
        initial_magic_level = MagicLevel(1, 0)
        initial_hp = Hp(100)
        initial_player = PlayerModel(initial_hp, initial_gun, initial_magic_level)
        self.player = initial_player
        self.level = None
        self.rng_system = RngSystem.get_instance()
        self.tech_upgrade_system = TechUpgradeSystem.get_instance()
        self.magic_upgrade_system = MagicUpgradeSystem.get_instance()

    def __update_model(self, model):
        self.player = model.player
        self.level = model.level
        self.rng_system.set_state(model.rng_system.get_state())
        self.tech_upgrade_system.set_state(model.tech_upgrade_system.get_state())
        self.magic_upgrade_system.set_state(model.magic_upgrade_system.get_state())

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
        target_file = open(f"/tmp/{SAVE_FILE_NAME}", "wb")
        pickle.dump(self, target_file)
        target_file.close()

    # Deserialize with pickle
    def load(self):
        source_file = open(f"/tmp/{SAVE_FILE_NAME}", "rb")
        previous_model = pickle.load(source_file)
        source_file.close()
        self.__update_model(previous_model)

    def save_exists(self):
        return os.path.exists(f"/tmp/{SAVE_FILE_NAME}")


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
