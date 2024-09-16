from pygame import mixer

class Song:
    """
    title: Song title.
    artist: Song artist.
    duration: Length of song in seconds.
    file: Music file location.
    timestamps: List of timestamps and lyrics formatted as [[timestamp, lyric, wpm], ...]
    lyrics: The lyrics of the song, padded with empty strings at start and end.
    wpm_list: The WPM required to type each lyric.
    """

    def __init__(self, title: str, artist: str, duration: int, file: str, timestamps: list[list], lyrics: list[str], max_wpm: int, average_wpm: int):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.file = file
        self.timestamps = timestamps
        self.lyrics = lyrics
        self.max_wpm = max_wpm
        self.average_wpm = average_wpm

    def play(self):
        mixer.init()
        mixer.music.load(self.file)
        mixer.music.play()
        mixer.music.set_volume(0.2)

    def stop(self):
        mixer.music.stop()