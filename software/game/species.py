import random

SPECIES = {
    "gato_guina": {
        "name": "Gato Güiña",
        "color": (200, 160, 100),
        "facts": [
            "Es el felino más pequeño de América, pesa entre 1.5 y 2.5 kg.",
            "Habita en bosques templados del sur de Chile y Argentina.",
            "Está en peligro de extinción por pérdida de su hábitat.",
            "Se alimenta de roedores, aves y pequeños reptiles.",
            "Es un excelente trepador gracias a sus uñas retráctiles.",
            "Su nombre mapuche significa 'ladrón' por su maña al cazar.",
        ],
    },
    "chungungo": {
        "name": "Chungungo",
        "color": (100, 130, 150),
        "facts": [
            "Es la única nutria marina de Sudamérica.",
            "Habita en costas rocosas desde Perú hasta Cabo de Hornos.",
            "Se alimenta de peces, crustáceos y moluscos.",
            "Está en peligro de extinción por caza y contaminación.",
            "Puede sumergirse hasta 30 metros para buscar alimento.",
            "Su pelaje es tan denso que la aísla del agua helada.",
        ],
    },
    "ranita_darwin": {
        "name": "Ranita de Darwin",
        "color": (80, 180, 70),
        "facts": [
            "El macho incuba los huevos en su saco vocal.",
            "Habita en los bosques templados del sur de Chile.",
            "Mide solo 2.5 a 3.5 cm de largo.",
            "Está en peligro crítico por hongo quitridio.",
            "Charles Darwin la descubrió en su viaje del Beagle.",
            "Su camuflaje la hace casi invisible entre los musgos.",
        ],
    },
    "zorro_chilote": {
        "name": "Zorro Chilote",
        "color": (190, 130, 80),
        "facts": [
            "Es el cánido más pequeño de Chile.",
            "Solo habita en Chiloé y la Cordillera de Nahuelbuta.",
            "Se alimenta de frutos, roedores, aves e insectos.",
            "Está en peligro de extinción por pérdida de hábitat.",
            "A pesar de llamarse zorro, está emparentado con los lobos.",
            "Es omnívoro: come desde bayas hasta pequeños mamíferos.",
        ],
    },
}

SPECIES_KEYS = list(SPECIES.keys())


def get_random_fact(especie):
    facts = SPECIES[especie].get("facts", [])
    return random.choice(facts) if facts else None
