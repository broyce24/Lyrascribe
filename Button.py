import pygame



class Button:
    buttons = []
    active_buttons = []

    @staticmethod
    def clear_active_buttons():
        Button.active_buttons.clear()

    def __init__(self, img_file: str, size: tuple[int, int], center: tuple[int, int], func=lambda: None):
        self.img = pygame.transform.scale(pygame.image.load(img_file), size)
        self.img_mask = pygame.mask.from_surface(self.img)
        self.size = size
        self.pos = self.from_center_coords(center)
        self.center = center
        self.call = func
        Button.buttons.append(self)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.pos)
        Button.active_buttons.append(self)

    def is_clicked(self, pos):
        try:
            return self.img_mask.get_at(tuple(map(lambda i, j: i - j, pos, self.pos)))
        except IndexError:
            return False

    def click(self):
        self.call()

    def from_center_coords(self, center_pos):
        return center_pos[0] - self.size[0] / 2, center_pos[1] - self.size[1] / 2