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
SONG_FILE = 'songs/timber_music.mp3'
LYRICS_FILE = 'songs/timber_lyrics.txt'
SONG_NAME = SONG_FILE[SONG_FILE.find('/') + 1:SONG_FILE.find('.')] + str(time.time())[-6:-1]  # avoids overwriting jason files

def record():
    mixer.init()
    timestamps = [0]
    lyrics = ['']
    with open(LYRICS_FILE) as f:
        lyrics.extend(f.read().splitlines())
    mixer.music.load(SONG_FILE)
    input("Press enter to start recording. Then press enter the moment each lyric starts.")
    mixer.music.play()
    start = time.time()
    mixer.music.set_volume(0.1)
    line_num = 0

    # start generating timestamps
    while True:
        input(f"{line_num}: {lyrics[line_num]}")
        timestamps.append(time.time() - start)
        line_num += 1
        if line_num == len(lyrics) - 1:
            print(f"{line_num}: {lyrics[line_num]}")
            break
    # end of song. last lyric should display until the song ends.
    timestamps.append(sys.maxsize)
    lyrics.append('')

    with open('songs/' + SONG_NAME + '.json', 'w') as file:
        json.dump(obj=vars(Song(SONG_FILE, timestamps, lyrics)), fp=file)




if __name__ == '__main__':
    record()

