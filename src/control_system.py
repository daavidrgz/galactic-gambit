from enum import Enum, auto

# Enum de las acciones que hay
# Acciones posibles:
#   Disparar


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
            Actions.DISPARAR: pygame.J,
            Actions.IZQUIERDA: pygame.A,
            Actions.DERECHA: pygame.D,
            Actions.ARRIBA: pygame.W,
            Actions.ABAJO: pygame.S,
            Actions.PAUSA: pygame.P,
        }

    def get_instance():
        if ControlSystem.__instance is None:
            ControlSystem.__instance = ControlSystem()
        return ControlSystem.__instance

    # Funcion que recibe un valor del enum, y te devuelva si esta pulsado o no
    # Se puede hacer el polling cada vez que se llame a esa funcion
    def isActiveAction(self, action):
        keys = pygame.key.get_pressed()
        if keys[self.actions[action.name()]]:
            return True
        else:
            return False

    # Funcion para bindear una tecla a un enum,y que se guarde en un mapa
    def rebindAction(self, action, key):
        self.actions[action.name()] = key
