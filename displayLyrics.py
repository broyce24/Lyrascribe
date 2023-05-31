import pygame
import pygame_gui
import Song

pygame.init()

pygame.display.set_caption("Quick Start")
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))

manager = pygame_gui.UIManager((800, 600))
hello_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 275), (100, 50)), text="Next line", manager=manager
)
clock = pygame.time.Clock()
is_running = True

while is_running:
    test_song = Song("countingstars.txt")
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print(test_song.next_line())
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

"""def show_lyrics(lyric_file):
    with open(lyric_file) as lyrics:
        for line in lyrics:
            print(line)
            time.sleep(2)"""

# show_lyrics('countingstars.txt')
