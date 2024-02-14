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
RESTART_IMG = "resources/restart.png"
PLAY_IMG = "resources/play_button.png"
STOP_IMG = "resources/stop.png"
FONT_FILE = "resources/filled_font.ttf"

WIDTH = 750
HEIGHT = 550

PLAY_BUTTON_SIZE = (50, 50)
PLAY_BUTTON_LOCATION = (400, 180)
STOP_BUTTON_SIZE = (50, 50)
STOP_BUTTON_LOCATION = (400, 180)
RESTART_BUTTON_DIM = (100, 100)
RESTART_BUTTON_LOCATION = (400, 400)
LYRIC_LOCATION = (25, 250)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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
        self.input_text = ""
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
        pygame.display.set_caption("LyricTyper")
        self.bg_img = pygame.image.load(BG_IMG)
        self.bg_img = pygame.transform.scale(self.bg_img, (750, 550))

    def draw_text(self, text, pos, font_size, text_color):
        """
        if "pos" is tuple, then that position is the top left corner of the text. If a single int, then text is centered
        at that y-coordinate.
        """
        font = pygame.font.Font(FONT_FILE, font_size)
        text_surface = font.render(text, True, text_color)
        if isinstance(pos, tuple):
            self.screen.blit(text_surface, pos)
            pygame.display.update()
            return pos
        self.screen.blit(text_surface, text_surface.get_rect(center=(WIDTH / 2, pos)))
        pygame.display.update()
        return text_surface.get_rect(center=(WIDTH / 2, pos))

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
        self.draw_text("LyricTyper", 80, 72, self.color_heading)
        pygame.display.update()

    def draw_playing_screen(self):
        self.draw_bg()
        self.stop_button.draw(self.screen)
        pygame.display.update()

    def play_song(self):
        self.state = "Playing"
        self.draw_playing_screen()
        self.song_playing = True
        EXAMPLE_SONG.play()

    def stop_song(self):
        self.state = "Menu"
        EXAMPLE_SONG.stop()
        self.restart_game()

    def restart_game(self):
        self.start_time = 0
        self.total_time = 0
        self.wpm = 0
        self.draw_menu_screen()
        self.play_button.draw(self.screen)
        pygame.display.update()
        self.state = "Menu"

    def run(self):

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

            if self.state == "Menu":
                self.restart_game()

            elif self.state == "Playing":

                clock1 = pygame.time.Clock()
                textinput = pygame_textinput.TextInputVisualizer(font_object=pygame.font.Font(FONT_FILE, LYRIC_SIZE),
                                                                 font_color=BLACK,
                                                                 cursor_width=0)
                index = 0
                start = time.time()
                current_lyric = ''

                while self.state == "Playing":
                    if not pygame.mixer.music.get_busy():
                        self.state = "Results"
                    events = pygame.event.get()
                    textinput.update(events)
                    self.draw_playing_screen()
                    lyric_rect = self.draw_text(current_lyric, LYRIC_LOCATION[1], LYRIC_SIZE,
                                                BLACK)
                    # user input typing
                    self.screen.blit(textinput.surface, lyric_rect)

                    if time.time() - start >= EXAMPLE_SONG.timestamps[index]:
                        textinput.value = ""
                        textinput.font_color = WHITE  # this does nothing, yet it fixes a bug
                        current_lyric = EXAMPLE_SONG.lyrics[index]
                        index += 1
                        print("new index:", index)

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
                    pygame.display.update()
                    clock1.tick(30)

            elif self.state == "Results":
                self.draw_bg()
                self.draw_text("You made it all the way through!", 100, 40, WHITE)
                # draw stats

            pygame.display.update()
            clock.tick(30)


if __name__ == "__main__":
    Typer().run()
