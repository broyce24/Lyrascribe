from Song import Song
import sys
from pygame import mixer
import time
import json
'''
Allows the user to create a song object with delays from a lyrics file.
Outputs a file with the song's lyrics and delays.
Press enter when each lyric starts.
'''
SONG_FILE = 'songs/umbrella_music.mp3'
LYRICS_FILE = 'songs/umbrella_lyrics_full.txt'
SONG_NAME = '4435243'

def record():
    mixer.init()
    delays = [0]
    lyrics = ['']
    with open(LYRICS_FILE) as f:
        lyrics.extend(f.read().splitlines())
    mixer.music.load(SONG_FILE)
    input("Press enter to start recording.")
    mixer.music.play()
    start = time.time()
    mixer.music.set_volume(0.1)
    line_num = 0

    # start generating timestamps
    while True:
        input(f"{line_num}: {lyrics[line_num]}")
        delays.append(time.time() - start)
        line_num += 1
        if line_num == len(lyrics) - 1:
            print(f"{line_num}: {lyrics[line_num]}")
            break
    # end of song. last lyric should display until the song ends.
    delays.append(sys.maxsize)
    lyrics.append('')

    with open('songs/' + SONG_NAME + '.json', 'w') as file:
        json.dump(obj=[delays, lyrics], fp=file)




if __name__ == '__main__':
    record()

