"""
NEVER OVERLAP BUTTONS!
ALL BUTTONS MUST BE CIRCLES, AND LOCATED BY THEIR CENTER
ONLY BLIT ONTO THE WHOLE WINDOW

Text will be a few pixels off when lyric contains an ', then once typed it fits itself correctly. This is due to the
background lyric rect being taller than the typing lyric rect until an apostrophe is typed, at which point they
become the same size and fit perfectly."""

import sys
import time
import json
import os
from functools import partial

import pygame
import pygame_textinput
import Levenshtein

from Button import Button, TextButton
from Song import Song
from Defaults import *


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
        self.song_buttons = []
        for i, song_name in enumerate(os.listdir('songs/json_files')):
            with open(os.path.join('songs/json_files', song_name), 'r') as file:
                curr_song = json.load(file, object_hook=lambda dct: Song(dct['title'], dct['artist'], dct['duration'],
                                                                         dct['file'],
                                                                         dct['timestamps'], dct['lyrics']))
                self.songs.append(curr_song)
                self.song_buttons.append(TextButton(f"{curr_song.title} - {curr_song.max_wpm}", i * 80 + 200, 80, WHITE, partial(self.play_song, curr_song)))

        self.songs.sort(key=lambda song: song.max_wpm)

        # Buttons
        self.play_button = Button(PLAY_IMG, PLAY_SIZE, PLAY_LOCATION, self.play_game)
        self.restart_button = Button(RESTART_IMG, RESTART_SIZE, RESTART_LOCATION, lambda: self.play_song(self.current_song))
        self.stop_button = Button(STOP_IMG, STOP_SIZE, STOP_LOCATION, self.stop_song)
        self.main_menu_button = Button(MAIN_MENU_IMG, MAIN_MENU_SIZE, MAIN_MENU_LOCATION, self.return_to_menu)

        # Playing songs
        self.failure_rate = 1  # each lyric's accuracy must be above this to pass. For debug, keep -1
        self.reaction_time = 0.5
        self.current_index = 0
        self.start_time = 0
        self.total_accuracy = 0
        self.textinput = pygame_textinput.TextInputVisualizer(font_object=pygame.font.Font(FONT_FILE, LYRIC_SIZE),
                                                              font_color=WHITE,
                                                              cursor_width=0)

    def draw_bg(self):
        self.screen.blit(self.bg_img, (0, 0))
        Button.clear_active_buttons()

    def draw_text(self, text, y_value, font_size, text_color, font_file=FONT_FILE):
        """
        Draws text centered at y_value.
        Returns the rect of the text that was drawn.
        """
        font = pygame.font.Font(font_file, font_size)
        text_surface = font.render(text, True, text_color)
        self.screen.blit(text_surface, text_surface.get_rect(center=(CENTER_X, y_value)))
        return text_surface.get_rect(center=(CENTER_X, y_value))

    def draw_menu_screen(self):
        self.draw_bg()
        self.draw_text(NAME, 160, 180, WHITE)
        self.play_button.draw(self.screen)

    def draw_song_select(self):
        self.draw_bg()
        self.draw_text("Song Select", 80, 100, WHITE)
        for song_button in self.song_buttons:
            song_button.draw(self.screen)

    def draw_playing_screen(self):
        self.draw_bg()
        self.stop_button.draw(self.screen)

    def draw_results_screen(self):
        self.draw_bg()
        self.draw_text("You made it all the way through!", 110, 100, WHITE)
        nonblank_lyrics = sum(bool(l) for l in self.current_song.lyrics)
        final_acc = round(self.total_accuracy / nonblank_lyrics * 100, 1)
        self.draw_text("Accuracy:" + str(final_acc) + "%",
                       760, 100, WHITE, NUMERIC_FONT_FILE)
        self.restart_button.draw(self.screen)
        self.main_menu_button.draw(self.screen)
        # displaying button rects debug
        # pygame.draw.rect(self.screen, BLACK, self.restart_button, 2)
        # pygame.draw.rect(self.screen, BLACK, self.main_menu_button, 2)

    def draw_failure_screen(self):
        self.draw_bg()
        self.draw_text("Oops! You didn't quite get that one...", 380, 100, WHITE)
        self.draw_text("Try again?", HEIGHT // 2 + 140, 100, WHITE)
        self.restart_button.draw(self.screen)
        self.main_menu_button.draw(self.screen)


    def play_game(self):
        self.state = "Song Select"

    def play_song(self, song):
        self.reset_song_values()
        self.state = "Playing"
        self.current_song = song
        self.current_song.play()
        self.start_time = time.time()

    def stop_song(self):
        self.state = "Song Select"
        self.current_song.stop()

    def return_to_menu(self):
        self.state = "Menu"

    def reset_song_values(self):
        self.current_index = 0
        self.textinput.value = ""
        self.start_time = 0
        self.total_accuracy = 0

    def ctrl_backspace(self):
        space_index = self.textinput.value.rfind(' ')
        if space_index == -1:
            self.textinput.value = ""
        else:
            self.textinput.value = self.textinput.value[:space_index + 2]
            # Need to include +2 because the textinput reader will also detect the backspace and delete extra char

    def ctrl_a(self):
        self.textinput.value = ""

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
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in Button.active_buttons:
                        if button.is_clicked(mouse_pos):
                            button.call()
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

            elif self.state == "Song Select":
                self.draw_song_select()

            elif self.state == "Playing":
                timestamp, lyric, wpm = self.current_song.timestamps[self.current_index]
                next_timestamp = self.current_song.timestamps[self.current_index + 1][0]

                self.draw_playing_screen()
                lyric_rect = self.draw_text(lyric, LYRIC_LOCATION[1], LYRIC_SIZE, BLACK)
                # draw the user inputted text
                # noinspection PyTypeChecker
                self.textinput.update(events)
                if ctrl_a:
                    self.textinput.value = ""
                    ctrl_a = False
                if lyric:
                    self.screen.blit(self.textinput.surface, lyric_rect)
                    self.draw_text("Current lyric: " + str(wpm) + " WPM",
                                   760, 100, WHITE, NUMERIC_FONT_FILE)

                # display current lyric once timestamp is reached
                if time.time() - self.start_time >= next_timestamp - self.reaction_time:
                    # collect accuracy
                    if lyric:
                        current_acc = Levenshtein.ratio(self.textinput.value.lower(), lyric)
                        if current_acc < self.failure_rate:
                            self.current_song.stop()
                            self.state = "Failure"
                        self.total_accuracy += current_acc
                    self.textinput.value = ""
                    self.textinput.font_color = WHITE  # this fixes a bug
                    self.current_index += 1
                    if next_timestamp == self.current_song.duration:
                        self.current_song.stop()
                        self.state = "Results"

            elif self.state == "Failure":
                self.draw_failure_screen()

            elif self.state == "Results":
                self.draw_results_screen()

            pygame.display.update()
            clock.tick(30)


if __name__ == "__main__":
    Typer().run()
