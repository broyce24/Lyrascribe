import pygame
import sys, time, random

background_image = 'background.jpg'
sentences_file = 'countingstars.txt'
restart_logo = 'restart.png'


def in_typing_box(x, y):
    return 50 <= x <= 650 and 200 <= y <= 250


def get_sentence():
    return random.choice(open(sentences_file).read().split('\n'))


class Type_Game:
    def __init__(self):
        self.running = False
        self.color_heading = (255, 255, 255)
        self.color_text = (235, 230, 232)
        self.color_results = (216, 222, 146)
        self.w = 750
        self.h = 550
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.active = False
        self.results = "Type:0 ~ Accuracy:0 % ~ Words Per Minute:0"
        self.accuracy = "0%"
        self.end = False
        self.wpm = 0
        self.input_text = ''
        self.word = ''
        self.start_time = 0
        self.restart_img = pygame.transform.scale(pygame.image.load(restart_logo), (200, 100))
        self.total_time = 0
        self.input_rect = pygame.Rect(50, 200, 650, 50)
        self.reset = True
        self.y_level_text = 225
        pygame.init()
        pygame.display.set_caption("Typing Game")
        self.bg_img = pygame.image.load(background_image)
        self.bg_img = pygame.transform.scale(self.bg_img, (750, 550))

    def write_text(self, screen, text, y, f_size, text_color):
        font_family = pygame.font.Font("Roboto-Regular.ttf", f_size)
        text_surface = font_family.render(text, 1, text_color)
        text_box = text_surface.get_rect(center=(self.w / 2, y))
        screen.blit(text_surface, text_box)
        pygame.display.flip()

    def reset_text_box(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_rect)
    def show_result(self, screen):
        if not self.end:
            self.total_time = time.time() - self.start_time
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = (count * 100) / len(self.word)
            self.wpm = (len(self.input_text) * 60) / (5 * self.total_time)
            self.end = True
            self.results = "Time: " + str(round(self.total_time)) + " secs ~ Accuracy: " + str(
                round(self.accuracy)) + "% ~ WPM: " + str(round(self.wpm))
            screen.blit(self.restart_img, (self.w / 2 - 70, self.h - 130))
            pygame.display.flip()

    def redraw_bg(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.write_text(self.screen, "Typing Game", 80, 72, self.color_heading)
    def restart_game(self):
        # time.sleep(1)
        self.reset = False
        self.end = False
        self.input_text = ''
        self.start_time = 0
        self.total_time = 0
        self.wpm = 0
        self.screen.fill((0, 0, 0)) # Clears the images from screen
        self.redraw_bg()
        # pygame.draw.rect(self.screen, (255, 190, 20), (50, 200, 650, 50), 3)
        # self.write_text(self.screen, self.word, 175, 24, self.color_text)
        pygame.display.flip()

    def run(self):
        self.restart_game()
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if in_typing_box(x, y):
                        self.active = True
                        self.input_text = ''
                        self.start_time = time.time()
                    if 310 <= x <= 510 and y >= 390 and self.end:
                        self.restart_game()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_result(self.screen)
                            print(self.results)
                            self.write_text(self.screen, self.results, 350, 28, self.color_results)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            self.input_text += event.unicode
            self.reset_text_box()
            text_surface = pygame.font.Font("Roboto-Regular.ttf", 24).render(self.input_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y+5))
            self.input_rect.w = max(100, text_surface.get_width()+10)
            pygame.display.flip()
            clock.tick(60)


if __name__ == '__main__':
    Type_Game().run()
