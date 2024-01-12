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

BG_IMG = "resources/background2.jpg"
LYRICS_TXT = "resources/countingstars.txt"
RESTART_IMG = "resources/restart.png"
PLAY_IMG = "resources/play_button.png"
STOP_IMG = "resources/stop.png"
FONT_FILE = "resources/outlined_font.ttf"

WIDTH = 750
HEIGHT = 550

PLAY_BUTTON_SIZE = (50, 50)
PLAY_BUTTON_LOCATION = (400, 180)
STOP_BUTTON_SIZE = (50, 50)
STOP_BUTTON_LOCATION = (400, 180)
RESTART_BUTTON_DIM = (100, 100)
RESTART_BUTTON_LOCATION = (400, 400)
LYRIC_LOCATION = (25, 250)
LYRIC_COLOR = (2, 2, 2)
LYRIC_SIZE = 40


class Typer:
    def __init__(self):
        self.state = "Menu"
        self.running = False
        self.color_heading = (255, 255, 255)
        self.color_text = (235, 230, 232)
        self.color_results = (216, 222, 146)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.song_playing = False
        self.results = "Type:0 ~ Accuracy:0 % ~ Words Per Minute:0"
        self.accuracy = "0%"
        self.wpm = 0
        self.word = ""
        self.start_time = 0
        self.play_button = Button(PLAY_IMG, PLAY_BUTTON_SIZE, PLAY_BUTTON_LOCATION, self.play_song)
        self.restart_button = Button(RESTART_IMG, RESTART_BUTTON_DIM, RESTART_BUTTON_LOCATION, self.restart_game)
        self.stop_button = Button(STOP_IMG, STOP_BUTTON_SIZE, STOP_BUTTON_LOCATION, self.stop_song)
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

    def draw_text(self, text, pos, font_size, text_color):
        """
        if "pos" is tuple, then that position is the top left corner of the text. If a single int, then text is centered at that y-coordinate.
        """
        text_surface = pygame.font.Font(FONT_FILE, font_size).render(text, True, text_color)
        if isinstance(pos, tuple):
            self.screen.blit(text_surface, pos)
            return
        self.screen.blit(text_surface, text_surface.get_rect(center=(WIDTH / 2, pos)))
        pygame.display.flip()

    def show_result(self):
        pass
        self.total_time = time.time() - self.start_time
        count = 0
        for i, c in enumerate(self.word):
            if self.input_text[i] == c:
                count += 1
        self.accuracy = (count * 100) / len(self.word)
        self.wpm = (len(self.input_text) * 60) / (5 * self.total_time)
        self.results = "Time: " + str(round(self.total_time)) + " secs ~ Accuracy: " + str(
            round(self.accuracy)) + "% ~ WPM: " + str(round(self.wpm))
        self.restart_button.draw(self.screen)
        pygame.display.flip()

    def draw_bg(self):
        self.screen.blit(self.bg_img, (0, 0))
        Button.clear_active_buttons()

    def draw_menu_screen(self):
        self.draw_bg()
        self.draw_text("Typing Game", 80, 72, self.color_heading)

    def draw_playing_screen(self):
        self.draw_bg()
        self.stop_button.draw(self.screen)

    def play_song(self):
        self.state = "Playing"
        self.song_playing = True
        self.draw_playing_screen()
        self.start_time = time.time()
        EXAMPLE_SONG.play()


    def stop_song(self):
        self.state = "Menu"
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
        self.start_time = 0
        self.total_time = 0
        self.wpm = 0
        self.draw_menu_screen()
        self.play_button.draw(self.screen)
        pygame.display.update()
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
                    for button in Button.active_buttons:
                        if button.is_clicked(pos):
                            button.click()
                            break

            if self.state == "Playing":
                textinput = pygame_textinput.TextInputVisualizer
                index = 0
                t1 = pygame.time.get_ticks()
                self.draw_text(EXAMPLE_SONG.lyrics[index], LYRIC_LOCATION[1], LYRIC_SIZE, LYRIC_COLOR)
                while self.state == "Playing":
                    if pygame.time.get_ticks() - t1 >= EXAMPLE_SONG.delays[index] * 1000:
                        index += 1
                        t1 = pygame.time.get_ticks()
                        self.draw_playing_screen()
                        self.draw_text(EXAMPLE_SONG.lyrics[index], LYRIC_LOCATION[1], LYRIC_SIZE, LYRIC_COLOR)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONUP:
                            pos = pygame.mouse.get_pos()
                            for button in Button.active_buttons:
                                if button.is_clicked(pos):
                                    button.click()
                                    break
                    events = pygame.event.get()
                    pygame.display.update()
                    clock.tick(60)


            pygame.display.update()
            clock.tick(60)


if __name__ == "__main__":
    Typer().run()
