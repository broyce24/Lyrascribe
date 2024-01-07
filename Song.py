import pygame, time, threading

def play_music(mp3_file):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()


delays = [1.78,
          2.98,
          2.96,
          3.13,
          3.24,
          2.85,
          2.98,
          3.10,
          1.64,
          3.21,
          3.23,
          2.50,
          2.84,
          2.96,
          3.07,
          3.30,
          3.5]
lyrics = ["you have my heart",
          "we'll never be worlds apart",
          "maybe in magazines",
          "but you'll still be my star",
          "baby cause in the dark",
          "you can't see shiny cars",
          "and that's when you need me there",
          "with you I'll always share",
          "because",
          "when the sun shine, we shine together",
          "told you I'll be here forever",
          "said I'll always be your friend",
          "took an oath and I'm stick it out till the end",
          "now that it's raining more than ever",
          "know that we still have each other",
          "you can stand under my umbrella",
          "you can stand under my umbrella",]


def display_lyrics():
    initial_delay = 1.1
    time.sleep(initial_delay)
    for delay, lyric in zip(delays, lyrics):
        print(lyric)
        time.sleep(delay)


def wait_for_input():
    input()
    pygame.mixer.music.stop()


music_thread = threading.Thread(target=play_music, args=('umbrella_remix.mp3',))
#input_thread = threading.Thread(target=wait_for_input)
display_thread = threading.Thread(target=display_lyrics)

music_thread.start()
#input_thread.start()
display_thread.start()