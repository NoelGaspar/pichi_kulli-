from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class LifeStage(Enum):
    CACHORRO = "cachorro"
    JOVEN = "joven"
    ADULTO = "adulto"
    LIBERADO = "liberado"


@dataclass
class Animal:
    especie: str
    nombre: str = ""
    hambre: int = 30
    energia: int = 80
    felicidad: int = 70
    higiene: int = 80
    salud: int = 80
    etapa: LifeStage = LifeStage.CACHORRO
    triste: bool = False
    tiempo_total: float = 0.0
    vivo: bool = True
    liberable: bool = False
    durmiendo: bool = False
    sleep_start_min: float = 0.0

    def clamp_stats(self):
        for stat in ("hambre", "energia", "felicidad", "higiene", "salud"):
            setattr(self, stat, max(0, min(100, getattr(self, stat))))

    def update_triste(self):
        self.triste = self.felicidad <= 0
