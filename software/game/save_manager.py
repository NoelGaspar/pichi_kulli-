import json
import os

SAVE_FILE = "pichi_kulli_save.json"


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
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        return json.load(f)


def reset_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


def has_save():
    return os.path.exists(SAVE_FILE)
