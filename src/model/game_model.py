import os
import pickle

from constants.game_constants import (
    INITIAL_GUN_COOLDOWN,
    INITIAL_GUN_DAMAGE,
    INITIAL_GUN_N_BULLETS,
    INITIAL_GUN_OFFSET,
    INITIAL_GUN_SPEED,
    INITIAL_GUN_SPREAD,
    INITIAL_GUN_KNOCKBACK,
)
from entities.living.hp import Hp
from entities.living.player.player import Player
from mechanics.gun import Gun
from mechanics.magic.magic_level import MagicLevel
from mechanics.magic.magic_upgrade_system import MagicUpgradeSystem
from mechanics.technology.tech_upgrade_system import TechUpgradeSystem
from systems.rng_system import RngSystem
from utils.singleton import Singleton

# TODO: Cuidado con pushear escenas... Al volver de otra escena, hay que tener en cuenta que en la escena
# anterior haya cambiado el modelo y haya que refrescar sprites... si hacemos switch scene no nos afecta

SAVE_FILE_NAME = "savegame_ciie"
SAVE_FILE_DIR = ".gamedata"


class GameModel(metaclass=Singleton):
    def __init__(self):
        self.init_model()
        self.rng_system = RngSystem.get_instance()
        self.tech_upgrade_system = TechUpgradeSystem.get_instance()
        self.magic_upgrade_system = MagicUpgradeSystem.get_instance()

    def init_model(self):
        initial_gun = Gun(
            INITIAL_GUN_DAMAGE,
            INITIAL_GUN_COOLDOWN,
            INITIAL_GUN_SPEED,
            INITIAL_GUN_OFFSET,
            INITIAL_GUN_SPREAD,
            INITIAL_GUN_N_BULLETS,
            INITIAL_GUN_KNOCKBACK,
        )

        initial_magic_level = MagicLevelModel(1, 0)
        initial_hp = HpModel(2, 2)
        initial_player = PlayerModel(initial_hp, initial_gun, initial_magic_level)
        self.player = initial_player
        self.level = None

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
        if not os.path.exists(SAVE_FILE_DIR):
            os.mkdir(SAVE_FILE_DIR)
        target_file = open(f"{SAVE_FILE_DIR}/{SAVE_FILE_NAME}", "wb")
        pickle.dump(self, target_file)
        target_file.close()

    # Deserialize with pickle
    def load(self):
        source_file = open(f"{SAVE_FILE_DIR}/{SAVE_FILE_NAME}", "rb")
        previous_model = pickle.load(source_file)
        source_file.close()
        self.__update_model(previous_model)

    def save_exists(self):
        return os.path.exists(f"{SAVE_FILE_DIR}/{SAVE_FILE_NAME}")

    def delete_save(self):
        if self.save_exists():
            os.remove(f"{SAVE_FILE_DIR}/{SAVE_FILE_NAME}")


class PlayerModel:
    def __init__(self, hp, gun, magic_level):
        self.hp = hp
        self.magic_level = magic_level
        self.gun = gun

    def from_sprite(player_sprite):
        hp = HpModel.from_game_hp(player_sprite.hp)
        gun = player_sprite.gun
        magic_level = MagicLevelModel.from_game_magic_level(player_sprite.magic_level)
        return PlayerModel(hp, gun, magic_level)


class HpModel:
    def __init__(self, hp, max_hp):
        self.hp = hp
        self.max_hp = max_hp

    def from_game_hp(game_hp):
        hp = game_hp.hp
        max_hp = game_hp.max_hp
        return HpModel(hp, max_hp)


class MagicLevelModel:
    def __init__(self, level, experience):
        self.level = level
        self.experience = experience

    def from_game_magic_level(game_magic_level):
        level = game_magic_level.level
        experience = game_magic_level.experience
        return MagicLevelModel(level, experience)
