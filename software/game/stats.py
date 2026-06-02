from __future__ import annotations
from game.animal import Animal, LifeStage

DECAY_RULES = {
    "hambre":  {"interval": 10,  "change": 4},
    "energia": {"interval": 15, "change": -5},
    "felicidad": {"interval": 20, "change": -5},
    "higiene": {"interval": 20, "change": -5},
}

DEFAULT_INTERVAL = 10

STAGE_THRESHOLDS = [
    (1, LifeStage.JOVEN),
    (4, LifeStage.ADULTO),
]


class StatsManager:
    def __init__(self):
        self.last_decay = {stat: 0.0 for stat in DECAY_RULES}
        self.last_critical = 0.0

    def update(self, animal: Animal, game_minutes: float):
        sad_bonus = 2 if animal.triste else 0

        for stat, rule in DECAY_RULES.items():
            if animal.durmiendo and stat == "energia":
                continue

            interval = rule["interval"]
            if game_minutes - self.last_decay[stat] >= interval:
                self.last_decay[stat] += interval
                change = rule["change"]
                if change > 0:
                    change += sad_bonus
                else:
                    change -= sad_bonus
                current = getattr(animal, stat)
                setattr(animal, stat, current + change)

        if game_minutes - self.last_critical >= DEFAULT_INTERVAL:
            self.last_critical += DEFAULT_INTERVAL
            if animal.hambre >= 90:
                animal.salud -= 2
            if animal.higiene <= 20:
                animal.salud -= 2
            if animal.energia <= 0:
                animal.salud -= 1

        animal.clamp_stats()
        animal.update_triste()

    def update_stage(self, animal: Animal):
        days = animal.tiempo_total / (24.0 * 60.0)
        for threshold, stage in reversed(STAGE_THRESHOLDS):
            if days >= threshold:
                animal.etapa = stage
                break
        else:
            animal.etapa = LifeStage.CACHORRO

        animal.liberable = (
            days >= 5
            and animal.etapa == LifeStage.ADULTO
            and animal.salud >= 100
        )

    def reset(self):
        for k in self.last_decay:
            self.last_decay[k] = 0.0
        self.last_critical = 0.0
