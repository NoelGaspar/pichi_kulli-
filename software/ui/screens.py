import pygame
from game.animal import Animal, LifeStage
from game.actions import Action, apply_action
from game.time_system import GameTime
from game.stats import StatsManager
from game.species import SPECIES, SPECIES_KEYS, get_random_fact
from game.save_manager import save_game
from ui.widgets import Button, WHITE, GRAY, DARK, GREEN, RED, BLUE, LIGHT_BG
from ui.hud import GameHUD
from ui.assets import make_placeholder_sprite

W, H = 280, 240

LEFT_KEYS = {pygame.K_LEFT, pygame.K_a}
RIGHT_KEYS = {pygame.K_RIGHT, pygame.K_d}
ACCEPT_KEYS = {pygame.K_RETURN, pygame.K_SPACE}
BACK_KEYS = {pygame.K_ESCAPE}


def is_key(event, keys):
    return event.type == pygame.KEYDOWN and event.key in keys


class TitleScreen:
    def __init__(self):
        self.btn_start = Button((90, 160, 100, 36), "Comenzar", color=GREEN, font_size=16)
        self.clock = 0

    def handle_event(self, event):
        if is_key(event, ACCEPT_KEYS):
            return "select_species"
        if self.btn_start.handle_event(event):
            return "select_species"
        return None

    def update(self, dt):
        self.clock += dt

    def draw(self, surface):
        surface.fill(LIGHT_BG)
        font_title = pygame.font.SysFont("sans", 28, bold=True)
        font_sub = pygame.font.SysFont("sans", 12)

        ts = font_title.render("Pichi-Kulliñ", True, GREEN)
        tw, th = ts.get_size()
        surface.blit(ts, ((W - tw) // 2, 50))

        lines = [
            "Cuida una especie nativa",
            "de Chile hasta liberarla",
        ]
        for i, line in enumerate(lines):
            ts = font_sub.render(line, True, GRAY)
            tw = ts.get_size()[0]
            surface.blit(ts, ((W - tw) // 2, 100 + i * 18))

        self.btn_start.draw(surface, selected=True)

        ts = font_sub.render("ENTER para comenzar", True, DARK)
        tw = ts.get_size()[0]
        surface.blit(ts, ((W - tw) // 2, 215))
        ts = font_sub.render("← → para navegar", True, DARK)
        tw = ts.get_size()[0]
        surface.blit(ts, ((W - tw) // 2, 225))


class SelectScreen:
    def __init__(self):
        self.selected_idx = 0
        self.buttons = []
        self._make_buttons()

    def _make_buttons(self):
        self.buttons = []
        bw, bh = 110, 80
        gap = 16
        total_w = 2 * bw + gap
        start_x = (W - total_w) // 2
        start_y = 42

        for i, key in enumerate(SPECIES_KEYS):
            col = i % 2
            row = i // 2
            x = start_x + col * (bw + gap)
            y = start_y + row * (bh + 12)
            info = SPECIES[key]
            btn = Button((x, y, bw, bh), info["name"], color=info["color"], font_size=11)
            self.buttons.append((btn, key))

    def handle_event(self, event):
        if is_key(event, LEFT_KEYS):
            self.selected_idx = (self.selected_idx - 1) % len(self.buttons)
        elif is_key(event, RIGHT_KEYS):
            self.selected_idx = (self.selected_idx + 1) % len(self.buttons)
        elif is_key(event, ACCEPT_KEYS):
            _, key = self.buttons[self.selected_idx]
            return ("select", key)

        for i, (btn, key) in enumerate(self.buttons):
            if btn.handle_event(event):
                self.selected_idx = i
                return ("select", key)
        return None

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(LIGHT_BG)
        font = pygame.font.SysFont("sans", 16, bold=True)
        ts = font.render("Elige tu especie", True, WHITE)
        tw = ts.get_size()[0]
        surface.blit(ts, ((W - tw) // 2, 15))

        for i, (btn, key) in enumerate(self.buttons):
            btn.draw(surface, selected=(i == self.selected_idx))
            sprite = make_placeholder_sprite(key, 36)
            sx = btn.rect.x + (btn.rect.w - 36) // 2
            sy = btn.rect.y + 22
            surface.blit(sprite, (sx, sy))

        font_small = pygame.font.SysFont("sans", 10)
        ts = font_small.render("← → navegar   ENTER aceptar", True, DARK)
        tw = ts.get_size()[0]
        surface.blit(ts, ((W - tw) // 2, H - 14))


class GameScreen:
    def __init__(self, especie, save_data=None):
        self.animal = Animal(especie=especie)
        self.game_time = GameTime()
        self.stats_mgr = StatsManager()
        self.message = ""
        self.message_timer = 0
        self.paused = False
        self._save_timer = 0.0

        if save_data:
            self._restore(save_data)

        self.hud = GameHUD(self.animal)

    def _restore(self, data):
        for stat in ("hambre", "energia", "felicidad", "higiene", "salud"):
            setattr(self.animal, stat, data[stat])
        self.animal.triste = data["triste"]
        self.animal.tiempo_total = data["tiempo_total"]
        self.animal.vivo = data["vivo"]
        self.animal.liberable = data["liberable"]
        self.animal.durmiendo = data.get("durmiendo", False)
        self.animal.sleep_start_min = data.get("sleep_start_min", 0.0)
        stage_map = {s.value: s for s in LifeStage}
        self.animal.etapa = stage_map.get(data.get("etapa", "cachorro"), LifeStage.CACHORRO)
        self.game_time.game_minutes = data.get("game_minutes", 0.0)
        self.stats_mgr.last_decay = {stat: data["game_minutes"] for stat in self.stats_mgr.last_decay}

    def _save(self):
        save_game(self.animal, self.game_time.get_minutes())

    def _wake_up(self):
        self.animal.durmiendo = False
        apply_action(self.animal, Action.DORMIR)
        self.message = f"{self.animal.especie} despertó con energía!"
        self.message_timer = 2.0
        self._save()

    def handle_event(self, event):
        if is_key(event, BACK_KEYS):
            self._save()
            return "title"

        if is_key(event, LEFT_KEYS):
            self.hud.navigate_left()
        elif is_key(event, RIGHT_KEYS):
            self.hud.navigate_right()
        elif is_key(event, ACCEPT_KEYS):
            action = self.hud.get_selected_action()
            return self._trigger_action(action)

        action = self.hud.handle_event(event)
        if action:
            return self._trigger_action(action)

        if self.animal.salud <= 0 and self.animal.vivo:
            self.animal.vivo = False
            return "rescate"

        return None

    def _trigger_action(self, action):
        if self.animal.durmiendo:
            if action == Action.DORMIR:
                self._wake_up()
            else:
                self.message = f"{self.animal.especie} está durmiendo..."
                self.message_timer = 1.5
            return None

        if action == Action.LIBERAR and self.animal.liberable:
            self._save()
            return "liberacion"

        if action == Action.APRENDER:
            fact = get_random_fact(self.animal.especie)
            if fact:
                self.message = fact
                self.message_timer = 4.0
            apply_action(self.animal, action)
            self._save()
            return None

        if action == Action.JUGAR and self.animal.energia < 15:
            self.message = f"{self.animal.especie} está muy cansado para jugar."
            self.message_timer = 1.5
            return None

        if action == Action.DORMIR:
            self.animal.durmiendo = True
            self.animal.sleep_start_min = self.game_time.get_minutes()
            self.message = f"{self.animal.especie} se fue a dormir..."
            self.message_timer = 1.5
            self._save()
            return None

        result = apply_action(self.animal, action)
        if result == "ok":
            action_name = {
                Action.ALIMENTAR: "Alimentaste",
                Action.JUGAR: "Jugaste",
                Action.DORMIR: "Durmió",
                Action.LIMPIAR: "Limpiaste",
                Action.CURAR: "Curaste",
            }.get(action, "")
            self.message = f"{action_name} a {self.animal.especie}!"
            self.message_timer = 2.0
            self._save()
        return None

    def update(self, dt):
        if self.paused:
            return
        self.game_time.update(dt)
        self.animal.tiempo_total = self.game_time.get_minutes()
        self.stats_mgr.update(self.animal, self.game_time.get_minutes())
        self.stats_mgr.update_stage(self.animal)

        if self.animal.durmiendo:
            sleep_min = self.game_time.get_minutes() - self.animal.sleep_start_min
            if sleep_min >= 120:
                self._wake_up()

        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""

        self._save_timer += dt
        if self._save_timer >= 10.0:
            self._save_timer = 0.0
            self._save()

        if self.animal.salud <= 0 and self.animal.vivo:
            self.animal.vivo = False
            self._save()
            return "rescate"
        return None

    def draw(self, surface):
        self.hud.draw(surface, self.game_time.get_minutes())

        if self.message:
            font = pygame.font.SysFont("sans", 11)
            tw = font.size(self.message)[0]
            if tw > W - 10:
                font = pygame.font.SysFont("sans", 9)
            lines = []
            remaining = self.message
            while remaining:
                for split in range(len(remaining), 0, -1):
                    if font.size(remaining[:split])[0] <= W - 12:
                        lines.append(remaining[:split])
                        remaining = remaining[split:]
                        break
                else:
                    lines.append(remaining)
                    remaining = ""
            y = 109
            for line in lines:
                ts = font.render(line, True, GREEN)
                tw2 = ts.get_size()[0]
                surface.blit(ts, ((W - tw2) // 2, y))
                y += 12


class EndScreen:
    def __init__(self, ending_type: str):
        self.ending_type = ending_type
        self.timer = 6.0
        self.done = False

    def handle_event(self, event):
        if is_key(event, ACCEPT_KEYS | BACK_KEYS):
            return "title"
        return None

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0 and not self.done:
            self.done = True
            return "title"
        return None

    def draw(self, surface):
        surface.fill((10, 10, 20))
        font = pygame.font.SysFont("sans", 14, bold=True)
        font_small = pygame.font.SysFont("sans", 11)

        if self.ending_type == "rescate":
            lines = [
                ("RESCATE", GREEN),
                ("", None),
                ("Tu mascota se puso muy enferma.", GRAY),
                ("Un equipo de especialistas", GRAY),
                ("se hará cargo de su cuidado.", GRAY),
                ("", None),
                ("Recuerda: los animales silvestres", GRAY),
                ("no son mascotas.", (200, 200, 100)),
                ("", None),
                ("El juego se reiniciará...", DARK),
            ]
        else:
            lines = [
                ("LIBERACIÓN", (100, 255, 100)),
                ("", None),
                ("¡Has cumplido tu misión!", WHITE),
                ("", None),
                ("El equipo de especialistas", GRAY),
                ("devuelve al animal a su", GRAY),
                ("entorno natural.", GRAY),
                ("", None),
                ("Gracias por cuidar", (200, 200, 100)),
                ("nuestra fauna nativa.", (200, 200, 100)),
            ]

        y = 30
        for text, color in lines:
            if text == "":
                y += 10
                continue
            color = color or GRAY
            ts = font.render(text, True, color) if len(text) < 20 else font_small.render(text, True, color)
            tw = ts.get_size()[0]
            surface.blit(ts, ((W - tw) // 2, y))
            y += 22 if len(text) < 20 else 16

        ts = font_small.render("ENTER para continuar", True, DARK)
        tw = ts.get_size()[0]
        surface.blit(ts, ((W - tw) // 2, 215))
