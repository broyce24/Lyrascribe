"""
NEVER OVERLAP BUTTONS!
ALL BUTTONS MUST BE CIRCLES, AND LOCATED BY THEIR CENTER
ONLY BLIT ONTO THE WHOLE WINDOW

Text will be a few pixels off when lyric contains an ', then once typed it fits itself correctly. This is due to the background lyric rect being taller than the typing lyric rect until an apostrophe is typed, at which point they become the same size and fit perfectly. The
"""

# When song is clicked, draw play button
# self.play_button.draw(self.screen)

import sys
import time
import json
import os

import pygame
import pygame_textinput
import Levenshtein

from Button import Button
from Song import Song


BG_IMG = "resources/background2.jpg"
RESTART_IMG = "resources/restart_button.png"
PLAY_IMG = "resources/play_button.png"
STOP_IMG = "resources/stop.png"
MAIN_MENU_IMG = "resources/main_menu.png"
FONT_FILE = "resources/filled_font.ttf"
NUMERIC_FONT_FILE = "resources/Roboto-Regular.ttf"
SCREEN_DIM = (1600, 900)
# Use (1600, 900) for debugging
WIDTH, HEIGHT = SCREEN_DIM
CENTER_WIDTH, CENTER_HEIGHT = WIDTH // 2, HEIGHT // 2
NAME = "LyricTyper"

# Button info
PLAY_SIZE = (100, 100)
PLAY_LOCATION = (CENTER_WIDTH, 280)
STOP_SIZE = (100, 100)
STOP_LOCATION = (CENTER_WIDTH, 280)
RESTART_SIZE = (150, 150)
RESTART_LOCATION = (CENTER_WIDTH, CENTER_HEIGHT)
LYRIC_SIZE = 100
LYRIC_LOCATION = (25, 480)
MAIN_MENU_SIZE = (300, 80)
MAIN_MENU_LOCATION = (CENTER_WIDTH, 870)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Typer:
    def __init__(self):
        # Creating display
        self.screen = pygame.display.set_mode(SCREEN_DIM)
        pygame.init()
        pygame.display.set_caption(NAME)
        self.bg_img = pygame.transform.scale(pygame.image.load(BG_IMG), SCREEN_DIM)

        # Internal states
        self.state = "Menu"
        self.running = False

        # Loading songs
        self.songs = []
        for song_name in os.listdir('songs/json_files'):
            with open(os.path.join('songs/json_files', song_name), 'r') as file:
                self.songs.append(
                    json.load(file, object_hook=lambda dct: Song(dct['title'], dct['artist'], dct['file'],
                                                                 dct['timestamps'], dct['lyrics'], dct['wpm_list'])))
        self.current_song = self.songs[-1] # use this for debugging

        # Buttons
        self.play_button = Button(PLAY_IMG, PLAY_SIZE, PLAY_LOCATION, self.play_song)
        self.restart_button = Button(RESTART_IMG, RESTART_SIZE, RESTART_LOCATION, self.restart_song)
        self.stop_button = Button(STOP_IMG, STOP_SIZE, STOP_LOCATION, self.stop_song)
        self.main_menu_button = Button(MAIN_MENU_IMG, MAIN_MENU_SIZE, MAIN_MENU_LOCATION, self.return_to_menu)

        # Playing songs
        self.failure_rate = -1  # each lyric's accuracy must be above this to pass. debugging For testing, keep -1
        self.reaction_time = 0.5
        self.next_index = 0
        self.start_time = 0
        self.current_lyric = ""
        self.total_accuracy = 0
        self.nonblank_lyrics = 0
        self.on_final_lyric = False
        self.textinput = pygame_textinput.TextInputVisualizer(font_object=pygame.font.Font(FONT_FILE, LYRIC_SIZE),
                                                              font_color=WHITE,
                                                              cursor_width=0)

    def draw_bg(self):
        self.screen.blit(self.bg_img, (0, 0))
        Button.clear_active_buttons()

    def return_to_menu(self):
        # not finished
        self.state = "Menu"

    def draw_song_select(self):
        # debug song names
        # currently unused
        self.draw_bg()
        self.draw_text(NAME, 80, 72, WHITE)
        song_names = (
            "Umbrella", "Don't Stop Believing", "Tequila", "Last Friday Night", "You Belong With Me", "Love Story",
            "Let Her Go", "The Nights")
        colors = (
            (0, 255, 0),
            (131, 209, 0),
            (153, 165, 0),
            (152, 125, 0),
            (140, 87, 0),
            (121, 50, 0),
            (91, 20, 5),
            (56, 0, 0)

        )
        for i, song_name in enumerate(song_names):
            self.draw_text(song_name, 40 * i + 140, 100, colors[i])

    def draw_menu_screen(self):
        self.draw_bg()
        self.draw_text(NAME, 160, 180, WHITE)
        self.play_button.draw(self.screen)

    def draw_playing_screen(self):
        self.draw_bg()
        self.stop_button.draw(self.screen)

    def draw_results_screen(self):
        self.draw_bg()
        self.draw_text("You made it all the way through!", 110, 100, WHITE)
        final_acc = round(self.total_accuracy / self.nonblank_lyrics * 100, 1)
        self.draw_text("Accuracy:" + str(final_acc) + "%",
                       760, 100, WHITE, NUMERIC_FONT_FILE)
        self.restart_button.draw(self.screen)
        self.main_menu_button.draw(self.screen)

    def draw_failure_screen(self):
        self.current_song.stop()
        self.draw_bg()
        self.draw_text("Oops! You didn't quite get that one...", 380, 100, WHITE)
        self.draw_text("Try again?", HEIGHT // 2 + 140, 100, WHITE)
        self.restart_button.draw(self.screen)
        self.main_menu_button.draw(self.screen)

    def play_song(self):
        self.reset_song_values()
        self.state = "Playing"
        self.current_song.play()
        self.start_time = time.time()

    def stop_song(self):
        self.state = "Menu"
        self.current_song.stop()

    def restart_song(self):
        self.play_song()

    def reset_song_values(self):
        self.textinput.value = ""
        self.next_index = 0
        self.start_time = 0
        self.current_lyric = ""
        self.total_accuracy = 0
        self.nonblank_lyrics = 0
        self.on_final_lyric = False

    def ctrl_backspace(self):
        space_index = self.textinput.value.rfind(' ')
        if space_index == -1:
            self.textinput.value = ""
        else:
            self.textinput.value = self.textinput.value[:space_index + 2]
            # Need to include +2 because the textinput reader will also detect the backspace and delete extra char

    def ctrl_a(self):
        self.textinput.value = ""

    def draw_text(self, text, y_value, font_size, text_color, font_file=FONT_FILE):
        """
        Draws text centered at y_value.
        Returns the rect of the text that was drawn.
        """
        font = pygame.font.Font(font_file, font_size)
        text_surface = font.render(text, True, text_color)
        self.screen.blit(text_surface, text_surface.get_rect(center=(CENTER_WIDTH, y_value)))
        return text_surface.get_rect(center=(CENTER_WIDTH, y_value))

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        # For lyric typing

        ctrl_a = False
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for button in Button.active_buttons:
                        if button.is_clicked(pos):
                            button.click()
                            break
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if event.key == pygame.K_BACKSPACE:
                            self.ctrl_backspace()
                        elif event.key == pygame.K_a:
                            self.ctrl_a()
                            ctrl_a = True

            if self.state == "Menu":
                self.draw_menu_screen()

            elif self.state == "Playing":
                self.draw_playing_screen()
                lyric_rect = self.draw_text(self.current_lyric, LYRIC_LOCATION[1], LYRIC_SIZE, BLACK)
                # draw the user inputted text
                # noinspection PyTypeChecker
                self.textinput.update(events)
                if ctrl_a:
                    self.textinput.value = ""
                    ctrl_a = False
                # debug
                self.screen.blit(self.textinput.surface, lyric_rect)
                print(lyric_rect, self.textinput.surface.get_rect())
                if not self.on_final_lyric and self.current_lyric:
                    self.draw_text("Current lyric: " + str(self.current_song.wpm_list[self.next_index - 1]) + " WPM", 760,
                                   100, WHITE, NUMERIC_FONT_FILE)

                # move onto next lyric, clearing input text
                if time.time() - self.start_time >= self.current_song.timestamps[self.next_index] - self.reaction_time:
                    # collect accuracy
                    if self.current_lyric:
                        current_acc = Levenshtein.ratio(self.textinput.value.lower(), self.current_lyric)
                        if current_acc < self.failure_rate:
                            self.state = "Failure"
                        self.total_accuracy += current_acc
                        self.nonblank_lyrics += 1
                    self.textinput.value = ""
                    self.textinput.font_color = WHITE  # this fixes a bug
                    self.current_lyric = self.current_song.lyrics[self.next_index]
                    self.next_index += 1
                    if self.current_song.timestamps[self.next_index] == sys.maxsize:
                        self.on_final_lyric = True
                elif not pygame.mixer.music.get_busy():
                    # final lyric's accuracy
                    current_acc = Levenshtein.ratio(self.textinput.value.lower(), self.current_lyric)
                    if current_acc < self.failure_rate:
                        self.state = "Failure"
                    else:
                        self.total_accuracy += current_acc
                        self.nonblank_lyrics += 1
                        self.state = "Results"

            elif self.state == "Failure":
                self.draw_failure_screen()

            elif self.state == "Results":
                self.draw_results_screen()

            pygame.display.update()
            clock.tick(30)


if __name__ == "__main__":
    Typer().run()
