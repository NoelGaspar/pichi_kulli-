import json
import os
import sys

SAVE_KEY = "pichi_kulli_save"


def _in_browser():
    return sys.platform == "emscripten"


def _get_storage():
    import platform
    return platform.window.localStorage


def save_game(animal, game_minutes):
    data = {
        "especie": animal.especie,
        "hambre": animal.hambre,
        "energia": animal.energia,
        "felicidad": animal.felicidad,
        "higiene": animal.higiene,
        "salud": animal.salud,
        "triste": animal.triste,
        "tiempo_total": animal.tiempo_total,
        "vivo": animal.vivo,
        "liberable": animal.liberable,
        "durmiendo": animal.durmiendo,
        "sleep_start_min": animal.sleep_start_min,
        "game_minutes": game_minutes,
    }
    if _in_browser():
        _get_storage().setItem(SAVE_KEY, json.dumps(data))
    else:
        with open(SAVE_KEY + ".json", "w") as f:
            json.dump(data, f, indent=2)


def load_game():
    if _in_browser():
        raw = _get_storage().getItem(SAVE_KEY)
        return json.loads(raw) if raw else None
    else:
        path = SAVE_KEY + ".json"
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return json.load(f)


def reset_save():
    if _in_browser():
        _get_storage().removeItem(SAVE_KEY)
    else:
        path = SAVE_KEY + ".json"
        if os.path.exists(path):
            os.remove(path)


def has_save():
    if _in_browser():
        return _get_storage().getItem(SAVE_KEY) is not None
    else:
        return os.path.exists(SAVE_KEY + ".json")
