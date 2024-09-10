import pygame
from Defaults import *


class Button:
    active_buttons = []

    @classmethod
    def clear_active_buttons(cls):
        Button.active_buttons.clear()

    def __init__(self, img_file: str, size: tuple[int, int], center: tuple[int, int], func=lambda: None):
        self.img = pygame.transform.scale(pygame.image.load(img_file), size)
        self.img_mask = pygame.mask.from_surface(self.img)
        self.blit_pos = (center[0] - size[0] / 2, center[1] - size[1] / 2)  # upper lefthand corner pixel location
        self.center = center
        self.call = func

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.blit_pos)
        Button.active_buttons.append(self)

    def is_clicked(self, mouse_pos):
        try:
            return self.img_mask.get_at(tuple(map(lambda i, j: i - j, mouse_pos, self.blit_pos)))
        except IndexError:
            return False

    def click(self):
        self.call()


class TextButton(Button):
    def __init__(self, text: str, y_value: int, font_size: int, text_color: str, func=lambda: None,
                 font_path: str = FONT_FILE):
        self.font_obj = pygame.font.Font(font_path, font_size)
        self.img = self.font_obj.render(text, True, text_color)
        self.rect = self.img.get_rect(center=(CENTER_X, y_value))
        self.rect.height = self.font_obj.get_height()
        self.call = func

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.rect)
        super().active_buttons.append(self)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
