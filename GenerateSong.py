from Song import Song
from pygame import mixer
import time
import json
from mutagen.mp3 import MP3

'''
Allows the user to create a song object with delays from a lyrics file.
Outputs a file with the song's lyrics and delays.
Press enter when each lyric starts.
'''
TITLE = 'short'
ARTIST = 'idk'
FILE = 'songs/short_music.mp3'
LYRICS = 'songs/short_lyrics.txt'
DURATION = MP3(FILE).info.length
# debug
avoid_overwrite = False
JSON_FILENAME = FILE[FILE.find('/') + 1:FILE.find('.')] + str(time.time())[-6:-1] if avoid_overwrite else '1'  # avoids overwriting json files

def record():
    mixer.init()
    timestamps = [0]
    lyrics = ['']
    wpm_list = []

    with open(LYRICS) as f:
        lyrics.extend(f.read().splitlines())
    mixer.music.load(FILE)
    input("Press enter to start recording. Then press enter the moment each lyric starts.")
    mixer.music.play()
    start = time.time()
    mixer.music.set_volume(0.2)
    line_num = 0

    # start generating timestamps
    while line_num < 5: # for debugging, while line_num < 5. When actually recording, make this infinite loop.
        input(f"{line_num}: {lyrics[line_num]}")
        timestamp = time.time() - start
        timestamps.append(timestamp)
        lyric_wpm = 0 if not lyrics[line_num] else round(len(lyrics[line_num]) / 5 * 60 / (timestamps[line_num + 1] - timestamps[line_num]))
        wpm_list.append(lyric_wpm)
        line_num += 1
        if line_num == len(lyrics) - 1:
            print(f"{line_num}: {lyrics[line_num]}")
            break
    # end of song. last lyric should display until the song ends.
    wpm_list.append(round(len(lyrics[line_num]) / 5 * 60 / (DURATION - timestamps[line_num])))
    timestamps.append(DURATION)
    lyrics.append('')
    wpm_list.append(0)
    reformatted_timestamps = [[t, l, w] for t, l, w in zip(timestamps, lyrics, wpm_list)]
    with open('songs/' + JSON_FILENAME + '.json', 'w') as file:
        json.dump(obj=vars(Song(TITLE, ARTIST, DURATION, FILE, reformatted_timestamps, lyrics)), fp=file)


if __name__ == '__main__':
    record()