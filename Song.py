from pygame import mixer


class Song:
    """
    file: filename
    delays: the duration of each lyric. First entry is the duration of no lyrics at the start of the song.
    lyrics: the lyrics of the song. First entry is empty.
    """
    def __init__(self, file, delays, lyrics):
        self.file = file
        self.delays = delays
        self.lyrics = lyrics

    def play(self):
        print("playing song")
        mixer.init()
        mixer.music.load(self.file)
        mixer.music.play()
        mixer.music.set_volume(0.1)

    def stop(self):
        print("stopping song")
        mixer.music.stop()


delays = [1.1,
          1.78,
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

lyrics = ["",
          "you have my heart",
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

EXAMPLE_SONG = Song("resources/umbrella_remix.mp3", delays, lyrics)
