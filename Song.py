from pygame import mixer
import json

class Song:
    """
    file: filename
    timestamps: the current lyric is displayed until we hit the timestamp.
    lyrics: the lyrics of the song. First entry is empty.
    """
    def __init__(self, music_file: str, timestamps: list[float], lyrics: list[str]):
        self.file = music_file
        self.timestamps = timestamps
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