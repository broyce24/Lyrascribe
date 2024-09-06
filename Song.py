from pygame import mixer


class Song:
    """
    title: Song title.
    artist: Song artist.
    duration: Length of song in seconds.
    file: Music file location.
    timestamps: List of timestamps and lyrics formatted as [[timestamp, lyric], ...]
    lyrics: The lyrics of the song, padded with empty strings at start and end.
    wpm_list: The WPM required to type each lyric.
    """

    def __init__(self, title: str, artist: str, duration: int, file: str, timestamps: list[float], lyrics: list[str], wpm_list: list[int]):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.file = file
        self.timestamps = timestamps
        self.lyrics = lyrics
        self.wpm_list = wpm_list
        self.max_wpm = max(wpm_list)
        self.nonempty_lyrics = sum(l != "" for l in lyrics)
        self.average_wpm = round(sum(wpm_list) / (self.nonempty_lyrics - 1))  # -1 cause last lyric's wpm doesn't count

    def play(self):
        mixer.init()
        mixer.music.load(self.file)
        mixer.music.play()
        mixer.music.set_volume(0.1)

    def stop(self):
        mixer.music.stop()


# debug
class Song2:
    """
    title: Song title.
    artist: Song artist.
    duration: Length of song in seconds.
    file: Music file location.
    timestamps: List of timestamps and lyrics formatted as [[timestamp, lyric, wpm], ...]
    lyrics: The lyrics of the song, padded with empty strings at start and end.
    wpm_list: The WPM required to type each lyric.
    """

    def __init__(self, title: str, artist: str, duration: int, file: str, timestamps: list[list[float], list[str], list[int]], lyrics: list[str]):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.file = file
        self.timestamps = timestamps
        self.lyrics = lyrics
        wpm_list = [entry[2] for entry in timestamps]
        self.max_wpm = max(wpm_list)
        nonempty_lyrics = sum(l != "" for l in lyrics)
        self.average_wpm = round(sum(wpm_list) / (nonempty_lyrics - 1))  # -1 cause last lyric's wpm doesn't count

    def play(self):
        mixer.init()
        mixer.music.load(self.file)
        mixer.music.play()
        mixer.music.set_volume(0.1)

    def stop(self):
        mixer.music.stop()