from pygame import mixer

class Song:
    """
    file: filename
    timestamps: the current lyric is displayed until we hit the timestamp.
    lyrics: the lyrics of the song. First entry is empty.
    """
    def __init__(self, title: str, artist: str, file: str, timestamps: list[float], lyrics: list[str], wpm_list: list[int]):
        self.title = title
        self.artist = artist
        self.file = file
        self.timestamps = timestamps
        self.lyrics = lyrics
        self.wpm_list = wpm_list
        self.nonempty_lyrics = sum(l != "" for l in lyrics)
        self.max_wpm = max(wpm_list)
        self.average_wpm = round(sum(self.wpm_list) / (self.nonempty_lyrics - 1)) # -1 cause last lyric's wpm doesn't count

    def play(self):
        mixer.init()
        mixer.music.load(self.file)
        mixer.music.play()
        mixer.music.set_volume(0.1)

    def stop(self):
        mixer.music.stop()