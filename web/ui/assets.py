import pygame
from game.species import SPECIES


def make_placeholder_sprite(especie: str, size: int = 64) -> pygame.Surface:
    color = SPECIES[especie]["color"]
    surf = pygame.Surface((size, size))
    surf.fill(color)
    darker = tuple(max(0, c - 40) for c in color)
    pygame.draw.ellipse(surf, darker, surf.get_rect(), 2)
    for _ in range(6):
        cx = size // 2
        cy = size // 2
        dx = (size // 4) + (size // 4)
        dy = (size // 4)
        pygame.draw.circle(surf, (255, 255, 255), (cx - 10, cy - 8), 5)
        pygame.draw.circle(surf, (255, 255, 255), (cx + 10, cy - 8), 5)
        pygame.draw.circle(surf, (0, 0, 0), (cx - 10, cy - 8), 2)
        pygame.draw.circle(surf, (0, 0, 0), (cx + 10, cy - 8), 2)
    font = pygame.font.SysFont("sans", 20)
    label = especie[:2].upper()
    ts = font.render(label, True, (255, 255, 255))
    tw, th = ts.get_size()
    surf.blit(ts, ((size - tw) // 2, (size - th) // 2 + 8))
    return surf


def make_mascara_sprite(size: int = 64) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, (50, 50, 50, 255), (size // 2, size // 2), size // 2 - 2)
    pygame.draw.circle(surf, (100, 100, 100, 255), (size // 2, size // 2), size // 2 - 4)
    font = pygame.font.SysFont("sans", 24)
    ts = font.render("?", True, (200, 200, 200))
    tw, th = ts.get_size()
    surf.blit(ts, ((size - tw) // 2, (size - th) // 2))
    return surf
