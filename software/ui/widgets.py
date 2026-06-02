import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK = (60, 60, 60)
GREEN = (60, 200, 60)
YELLOW = (220, 200, 40)
RED = (220, 40, 40)
BLUE = (40, 120, 200)
LIGHT_BG = (30, 30, 40)
HIGHLIGHT = (255, 255, 0)


class Button:
    def __init__(self, rect, label, color=BLUE, text_color=WHITE, font_size=12):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont("sans", font_size)
        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface, selected=False):
        c = tuple(min(255, cc + 30) for cc in self.color) if self.hovered else self.color
        pygame.draw.rect(surface, c, self.rect, border_radius=4)
        if selected:
            pygame.draw.rect(surface, HIGHLIGHT, self.rect, 3, border_radius=4)
        else:
            pygame.draw.rect(surface, WHITE, self.rect, 1, border_radius=4)
        ts = self.font.render(self.label, True, self.text_color)
        tw, th = ts.get_size()
        surface.blit(ts, (
            self.rect.x + (self.rect.w - tw) // 2,
            self.rect.y + (self.rect.h - th) // 2,
        ))


class ProgressBar:
    def __init__(self, rect, color=GREEN, bg_color=DARK):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.bg_color = bg_color
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = max(0, min(100, v))

    def get_color(self):
        if self._value < 25:
            return RED
        if self._value < 50:
            return YELLOW
        return GREEN

    def draw(self, surface, label="", show_value=False):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=3)
        fill_w = int(self.rect.w * self._value / 100)
        if fill_w > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.rect.h)
            pygame.draw.rect(surface, self.get_color(), fill_rect, border_radius=3)

        font = pygame.font.SysFont("sans", 10)
        if label:
            ls = font.render(label, True, WHITE)
            surface.blit(ls, (self.rect.x - 22, self.rect.y + 1))
        if show_value:
            vs = font.render(str(int(self._value)), True, WHITE)
            surface.blit(vs, (self.rect.right + 4, self.rect.y + 1))
