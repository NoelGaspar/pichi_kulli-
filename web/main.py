import asyncio
import sys

import pygame

from game.save_manager import has_save, load_game, reset_save
from ui.screens import TitleScreen, SelectScreen, GameScreen, EndScreen

W, H = 280, 240
SCALE = 2
WINDOW_W, WINDOW_H = W * SCALE, H * SCALE
FPS = 60


async def main():
    pygame.init()
    pygame.display.set_caption("Pichi-Kulliñ")
    display = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pygame.time.Clock()

    if "--reset" in sys.argv:
        reset_save()
        print("Partida eliminada.")

    if has_save():
        data = load_game()
        screen = GameScreen(data["especie"], save_data=data)
    else:
        screen = TitleScreen()

    internal = pygame.Surface((W, H))
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if isinstance(screen, GameScreen):
                    screen._save()
                running = False
                break

            result = screen.handle_event(event)
            if result:
                if result == "select_species":
                    screen = SelectScreen()
                elif isinstance(result, tuple) and result[0] == "select":
                    screen = GameScreen(result[1])
                elif result == "title":
                    screen = TitleScreen()
                elif result == "rescate":
                    reset_save()
                    screen = EndScreen("rescate")
                elif result == "liberacion":
                    reset_save()
                    screen = EndScreen("liberacion")

        result = screen.update(dt)
        if result:
            if result == "title":
                screen = TitleScreen()

        screen.draw(internal)

        scaled = pygame.transform.scale(internal, (WINDOW_W, WINDOW_H))
        display.blit(scaled, (0, 0))
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
