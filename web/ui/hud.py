import pygame
from game.animal import Animal, LifeStage
from game.actions import Action
from ui.widgets import Button, ProgressBar
from game.species import SPECIES

W, H = 280, 240

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK = (60, 60, 60)
LIGHT_BG = (30, 30, 40)
GREEN = (60, 200, 60)
BLUE = (40, 120, 200)
RED = (220, 40, 40)

STAGE_LABELS = {
    LifeStage.CACHORRO: "Cachorro",
    LifeStage.JOVEN: "Joven",
    LifeStage.ADULTO: "Adulto",
    LifeStage.LIBERADO: "Liberado",
}

SHORT_LABELS = {
    Action.ALIMENTAR: "Comer",
    Action.JUGAR: "Jugar",
    Action.DORMIR: "Dormir",
    Action.LIMPIAR: "Limp",
    Action.CURAR: "Curar",
    Action.APRENDER: "Leer",
    Action.LIBERAR: "Lib",
}

STAT_CONFIG = [
    ("hambre",  "H", (220, 60, 60)),
    ("energia", "E", (240, 200, 40)),
    ("felicidad", "F", (240, 100, 200)),
    ("higiene",  "G", (80, 200, 240)),
    ("salud",    "S", (60, 200, 60)),
]

SPRITE_SIZE = 80
SPRITE_Y = 62

STATS_Y = 178
STAT_BAR_H = 8
STAT_GAP = 4
ROW_H = STAT_BAR_H + STAT_GAP

COL_LEFT = 6
COL_RIGHT = 144
COL_W = 130

ICON_S = 10
ICON_Y_OFF = (STAT_BAR_H - ICON_S) // 2


class GameHUD:
    ALL_ACTIONS = [
        Action.ALIMENTAR,
        Action.JUGAR,
        Action.DORMIR,
        Action.LIMPIAR,
        Action.CURAR,
        Action.APRENDER,
    ]

    def __init__(self, animal):
        self.animal = animal
        self.selected_idx = 0
        self.buttons = []
        self._make_buttons()

    def _make_buttons(self):
        self.buttons = []
        btn_w, btn_h, gap = 38, 26, 4
        total_w = 6 * btn_w + 5 * gap
        start_x = (W - total_w) // 2
        actions_y = 214

        for i, action in enumerate(self.ALL_ACTIONS):
            x = start_x + i * (btn_w + gap)
            color = BLUE
            btn = Button((x, actions_y, btn_w, btn_h), SHORT_LABELS[action], color=color, font_size=10)
            self.buttons.append((btn, action))

    def navigate_left(self):
        self.selected_idx = (self.selected_idx - 1) % len(self.ALL_ACTIONS)

    def navigate_right(self):
        self.selected_idx = (self.selected_idx + 1) % len(self.ALL_ACTIONS)

    def handle_event(self, event):
        for i, (btn, _) in enumerate(self.buttons):
            if btn.handle_event(event):
                if i == 5 and self.animal.liberable:
                    return Action.LIBERAR
                return self.ALL_ACTIONS[i]
        return None

    def get_selected_action(self):
        action = self.ALL_ACTIONS[self.selected_idx]
        if action == Action.APRENDER and self.animal.liberable:
            return Action.LIBERAR
        return action

    def _draw_top_bar(self, surface, game_minutes):
        font = pygame.font.SysFont("sans", 11)
        title_font = pygame.font.SysFont("sans", 14, bold=True)

        name = SPECIES[self.animal.especie]["name"]
        stage_str = STAGE_LABELS.get(self.animal.etapa, "?")

        ts = title_font.render(f"{stage_str}", True, WHITE)
        tw, th = ts.get_size()
        bg = pygame.Rect(4, 3, tw + 4, th + 2)
        pygame.draw.rect(surface, (70, 70, 80), bg, border_radius=3)
        pygame.draw.rect(surface, GRAY, bg, 1, border_radius=3)
        surface.blit(ts, (6, 4))
        ts = title_font.render(name, True, (200, 200, 200))
        surface.blit(ts, (85, 4))

        days = game_minutes / (24 * 60)
        hours = (game_minutes % (24 * 60)) / 60
        mins = game_minutes % 60
        time_str = f"D{days:.1f} {int(hours):02d}:{int(mins):02d}"
        ts = font.render(time_str, True, GRAY)
        tw = ts.get_size()[0]
        surface.blit(ts, (W - tw - 6, 6))
        pygame.draw.line(surface, GRAY, (0, 22), (W, 22))

    def _draw_sprite(self, surface):
        from ui.assets import make_placeholder_sprite
        sprite_x = (W - SPRITE_SIZE) // 2
        sprite = make_placeholder_sprite(self.animal.especie, SPRITE_SIZE)
        surface.blit(sprite, (sprite_x, SPRITE_Y))
        font = pygame.font.SysFont("sans", 10)
        if self.animal.durmiendo:
            ts = font.render("DURMIENDO", True, (100, 180, 255))
            tw = ts.get_size()[0]
            surface.blit(ts, ((W - tw) // 2, SPRITE_Y + SPRITE_SIZE + 1))
        elif self.animal.triste:
            ts = font.render("TRISTE", True, RED)
            surface.blit(ts, (sprite_x, SPRITE_Y + SPRITE_SIZE + 1))
        if self.animal.liberable and not self.animal.durmiendo:
            ts = font.render("LISTO PARA LIBERAR!", True, (100, 255, 100))
            tw = ts.get_size()[0]
            surface.blit(ts, ((W - tw) // 2, SPRITE_Y + SPRITE_SIZE + 1))

    def _draw_stats(self, surface):
        font = pygame.font.SysFont("sans", 9)
        val_font = pygame.font.SysFont("sans", 9, bold=True)
        bar_inner_w = COL_W - ICON_S - 4 - 24

        pairs = [
            (0, 1),
            (2, 3),
            (4, None),
        ]

        for row_i, (left_idx, right_idx) in enumerate(pairs):
            row_y = STATS_Y + row_i * ROW_H

            for col_i, idx in enumerate([left_idx, right_idx]):
                if idx is None:
                    continue
                key, letter, color = STAT_CONFIG[idx]
                col_x = COL_LEFT if col_i == 0 else COL_RIGHT
                val = getattr(self.animal, key)

                icon_r = pygame.Rect(col_x, row_y + ICON_Y_OFF, ICON_S, ICON_S)
                pygame.draw.rect(surface, color, icon_r, border_radius=2)
                ls = font.render(letter, True, WHITE)
                lw = ls.get_size()[0]
                surface.blit(ls, (col_x + (ICON_S - lw) // 2, row_y + ICON_Y_OFF - 1))

                bar_x = col_x + ICON_S + 4
                bar_r = pygame.Rect(bar_x, row_y, bar_inner_w, STAT_BAR_H)
                bar_bg = (50, 50, 60)
                pygame.draw.rect(surface, bar_bg, bar_r, border_radius=2)

                fill_w = int(bar_inner_w * val / 100)
                if fill_w > 0:
                    if val < 25:
                        bar_c = RED
                    elif val < 50:
                        bar_c = (240, 200, 40)
                    else:
                        bar_c = GREEN
                    fill_r = pygame.Rect(bar_x, row_y, fill_w, STAT_BAR_H)
                    pygame.draw.rect(surface, bar_c, fill_r, border_radius=2)

                vs = val_font.render(str(int(val)), True, WHITE)
                vx = col_x + COL_W - 22
                surface.blit(vs, (vx, row_y))

    def draw(self, surface, game_minutes):
        surface.fill(LIGHT_BG)
        self._draw_top_bar(surface, game_minutes)
        self._draw_sprite(surface)
        self._draw_stats(surface)

        for i, (btn, _) in enumerate(self.buttons):
            if self.animal.durmiendo:
                if i == 2:
                    btn.color = GREEN
                    btn.label = "Desp"
                else:
                    btn.color = GRAY
            elif i == 5 and self.animal.liberable:
                btn.color = GREEN
                btn.label = "Lib"
            elif i == 5:
                btn.color = BLUE
                btn.label = "Leer"
            else:
                btn.color = BLUE
            btn.draw(surface, selected=(i == self.selected_idx))
