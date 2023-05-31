class Song:
    def __init__(self, lyrics_file) -> None:
        with open(lyrics_file) as f:
            self.song_lyrics = f.readlines()

    def next_line(self):
        return self.song_lyrics.pop(0)
