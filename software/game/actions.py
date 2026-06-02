from __future__ import annotations
from enum import Enum, auto


class Action(Enum):
    ALIMENTAR = auto()
    JUGAR = auto()
    DORMIR = auto()
    LIMPIAR = auto()
    CURAR = auto()
    APRENDER = auto()
    LIBERAR = auto()


ACTION_EFFECTS = {
    Action.ALIMENTAR: {"hambre": -20, "felicidad": 5},
    Action.JUGAR: {"felicidad": 15, "energia": -10, "hambre": 5},
    Action.DORMIR: {"energia": 30, "felicidad": 5, "hambre": 5},
    Action.LIMPIAR: {"higiene": 20, "felicidad": 5},
    Action.CURAR: {"salud": 20},
    Action.APRENDER: {"felicidad": 10},
    Action.LIBERAR: {},
}


def apply_action(animal, action):
    if action == Action.LIBERAR:
        if animal.liberable:
            return "liberar"
        return None

    effects = ACTION_EFFECTS[action]
    for stat, delta in effects.items():
        current = getattr(animal, stat)
        setattr(animal, stat, current + delta)

    animal.clamp_stats()
    animal.update_triste()
    return "ok"
