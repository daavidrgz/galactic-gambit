from enum import Enum, auto

# Enum de las acciones que hay
# Acciones posibles:
#   Disparar


class ActionsEnum(Enum):
    DISPARAR = auto()
    ARRIBA = auto()
    ABAJO = auto()
    IZQUIERDA = auto()
    DERECHA = auto()
    PAUSA = auto()


class Actions:
    __instance = None

    # Diccionario con el mapeo inicial de acciones a teclas
    def __init__(self):
        self.actions = {
            ActionsEnum.DISPARAR: "J",
            ActionsEnum.IZQUIERDA: "A",
            ActionsEnum.DERECHA: "D",
            ActionsEnum.ARRIBA: "W",
            ActionsEnum.ABAJO: "S",
            ActionsEnum.PAUSA: "P",
        }

    def get_instance():
        if Actions.__instance is None:
            Actions.__instance = Actions()
        return Actions.__instance

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
