import pygame, time, threading


class Song:
    def __init__(self, initial_delay, delays, lyrics):
        self.initial_delay = initial_delay
        self.delays = delays
        self.lyrics = lyrics

    def play_music(self, mp3_file):
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play()

    def display_lyrics(self):
        time.sleep(self.initial_delay)
        for lyric_duration, lyric in zip(self.delays, self.lyrics):
            print(lyric)
            time.sleep(lyric_duration)

    def play(self):
        music_thread = threading.Thread(target=self.play_music, args=('umbrella_remix.mp3',))
        display_thread = threading.Thread(target=self.display_lyrics)
        music_thread.start()
        display_thread.start()

initial_delay = 1.1
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
          "you can stand under my umbrella", ]

Song(initial_delay, delays, lyrics).play()