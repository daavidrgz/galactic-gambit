from enum import Enum, auto
import pygame

# Enum de las acciones que hay
class Actions(Enum):
    DISPARAR = auto()
    ARRIBA = auto()
    ABAJO = auto()
    IZQUIERDA = auto()
    DERECHA = auto()
    PAUSA = auto()


class ControlSystem:
    __instance = None

    # Diccionario con el mapeo inicial de acciones a teclas
    def __init__(self):
        self.actions = {
            Actions.DISPARAR: pygame.K_j,
            Actions.IZQUIERDA: pygame.K_a,
            Actions.DERECHA: pygame.K_d,
            Actions.ARRIBA: pygame.K_w,
            Actions.ABAJO: pygame.K_s,
            Actions.PAUSA: pygame.K_p,
        }

    def get_instance():
        if ControlSystem.__instance is None:
            ControlSystem.__instance = ControlSystem()
        return ControlSystem.__instance

    # Funcion que recibe un valor del enum, y te devuelva si esta pulsado o no
    # Se puede hacer el polling cada vez que se llame a esa funcion
    def isActiveAction(self, action):
        return pygame.key.get_pressed()[self.actions[action]]

    # Funcion para bindear una tecla a un enum,y que se guarde en un mapa
    def rebindAction(self, action, key):
        self.actions[action] = key
