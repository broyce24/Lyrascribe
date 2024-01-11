"""
NEVER OVERLAP BUTTONS!
ALL BUTTONS MUST BE CIRCLES, AND LOCATED BY THEIR CENTER
ONLY BLIT ONTO THE WHOLE WINDOW
"""

import sys
import time

import pygame
import pygame_textinput

from Button import Button
from Song import EXAMPLE_SONG

BG_IMG = "resources/background.jpg"
LYRICS_TXT = "resources/countingstars.txt"
RESTART_IMG = "resources/restart.png"
PLAY_IMG = "resources/play_button.png"
STOP_IMG = "resources/stop_button.jpg"

WIDTH = 750
HEIGHT = 550

PLAY_BUTTON_SIZE = (50, 50)
PLAY_BUTTON_LOCATION = (400, 180)
STOP_BUTTON_SIZE = (50, 50)
STOP_BUTTON_LOCATION = (500, 180)
RESTART_BUTTON_DIM = (100, 100)
RESTART_BUTTON_LOCATION = (400, 400)


def in_typing_box(pos):
    x, y = pos
    return 50 <= x <= 650 and 200 <= y <= 250


class Typer:
    def __init__(self):
        self.state = "Menu"
        self.running = False
        self.color_heading = (255, 255, 255)
        self.color_text = (235, 230, 232)
        self.color_results = (216, 222, 146)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.song_playing = False
        self.h = 9
        self.results = "Type:0 ~ Accuracy:0 % ~ Words Per Minute:0"
        self.accuracy = "0%"
        self.end = False
        self.wpm = 0
        self.input_text = ""
        self.word = ""
        self.start_time = 0
        self.play_button = Button(PLAY_IMG, PLAY_BUTTON_SIZE, PLAY_BUTTON_LOCATION, self.play_song)
        self.restart_button = Button(RESTART_IMG, RESTART_BUTTON_DIM, RESTART_BUTTON_LOCATION, self.play_song)
        self.stop_button = Button(STOP_IMG, STOP_BUTTON_SIZE, STOP_BUTTON_LOCATION, self.restart_game)
        self.total_time = 0
        self.input_rect = pygame.Rect(50, 200, 650, 50)
        # Create TextInput-object
        self.textinput = pygame_textinput.TextInputVisualizer()
        self.reset = True
        self.y_level_text = 225
        pygame.init()
        pygame.display.set_caption("Typing Game")
        self.bg_img = pygame.image.load(BG_IMG)
        self.bg_img = pygame.transform.scale(self.bg_img, (750, 550))

    def draw_centered_text(self, text, y, font_size, text_color):
        pass
        font_family = pygame.font.Font("resources/Roboto-Regular.ttf", font_size)
        text_surface = font_family.render(text, True, text_color)
        text_box = text_surface.get_rect(center=(WIDTH / 2, y))
        self.screen.blit(text_surface, text_box)
        pygame.display.flip()

    def reset_text_box(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_rect)

    def show_result(self):
        pass
        if not self.end:
            self.total_time = time.time() - self.start_time
            count = 0
            for i, c in enumerate(self.word):
                if self.input_text[i] == c:
                    count += 1
            self.accuracy = (count * 100) / len(self.word)
            self.wpm = (len(self.input_text) * 60) / (5 * self.total_time)
            self.end = True
            self.results = "Time: " + str(round(self.total_time)) + " secs ~ Accuracy: " + str(
                round(self.accuracy)) + "% ~ WPM: " + str(round(self.wpm))
            self.restart_button.draw(self.screen)
            pygame.display.flip()

    def redraw_bg(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.draw_centered_text("Typing Game", 80, 72, self.color_heading)

    def play_song(self):
        self.song_playing = True
        self.stop_button.draw(self.screen)
        self.input_text = ""
        self.start_time = time.time()
        EXAMPLE_SONG.play("umbrella_remix.mp3")
        time.sleep(EXAMPLE_SONG.initial_delay)

        self.state = "Playing"
        # display_thread = threading.Thread(target=self.display_lyrics, args=())

    def stop_song(self):
        EXAMPLE_SONG.stop()
        self.restart_game()

    def display_lyrics(self):
        for lyric_duration, lyric in zip(EXAMPLE_SONG.delays, EXAMPLE_SONG.lyrics):
            text = pygame.font.Font("Roboto-Regular.ttf", 24).render(lyric, True, (84, 84, 84))
            self.screen.blit(text, self.input_rect)
            pygame.display.update()
            time.sleep(lyric_duration)
            exit()

    def restart_game(self):
        self.reset = False
        self.end = False
        self.input_text = ""
        self.start_time = 0
        self.total_time = 0
        self.wpm = 0
        self.screen.fill((0, 0, 0))  # Clears the images from screen
        self.redraw_bg()
        self.play_button.draw(self.screen)
        # pygame.draw.rect(self.screen, (255, 190, 20), (50, 200, 650, 50), 3)
        # self.write_text(self.screen, self.word, 175, 24, self.color_text)
        pygame.display.flip()
        self.state = "Menu"

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
                    pos = pygame.mouse.get_pos()
                    for button in Button.buttons:
                        if button.is_clicked(pos):
                            button.click()
                            break
                elif event.type == pygame.KEYDOWN:
                    if self.song_playing and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            # self.show_result(self.screen)
                            # print(self.results)
                            self.draw_centered_text(self.results, 350, 28, self.color_results)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            # self.input_text += event.unicode
                            pass

            if self.state == "Playing":
                self.run_game()

            # self.reset_text_box()
            self.textinput.update(pygame.event.get())
            self.screen.blit(self.textinput.surface, (10, 10))
            # text_surface = pygame.font.Font("Roboto-Regular.ttf", 24).render(self.input_text, True, (255, 255, 255))
            # self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
            # self.input_rect.w = max(100, text_surface.get_width() + 10)
            pygame.display.flip()
            clock.tick(60)

    state = "Menu"
    old_time = pygame.time.get_ticks()
    delay_index = 0
    lyric_index = 0

    def run_game(self):
        if self.old_time - pygame.time.get_ticks() > EXAMPLE_SONG.delays[self.delay_index * 1000]:
            self.delay_index += 1
            old_time = pygame.time.get_ticks()
            self.lyric_index += 1
            text = pygame.font.Font("Roboto-Regular.ttf", 24).render(EXAMPLE_SONG.lyrics[self.lyric_index], True,
                                                                     (84, 84, 84))
            self.screen.blit(text, self.input_rect)


if __name__ == "__main__":
    Typer().run()
