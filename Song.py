from pygame import mixer
import json
from mutagen.mp3 import MP3

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
        self.duration = MP3(music_file).info.length

    def play(self):
        print("playing song")
        mixer.init()
        mixer.music.load(self.file)
        mixer.music.play()
        mixer.music.set_volume(0.1)

    def stop(self):
        print("stopping song")
        mixer.music.stop()



serialized_file = 'songs/umbrella.json'
with open(serialized_file, 'r') as file:
    EXAMPLE_SONG = json.load(file, object_hook=lambda dct: Song(dct['file'], dct['timestamps'], dct['lyrics']))
#EXAMPLE_SONG = Song("songs/umbrella_music.mp3", original_delays, original_lyrics)