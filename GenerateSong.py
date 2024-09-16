from Song import Song
from pygame import mixer
import time
import json
from mutagen.mp3 import MP3

'''
Lyrics file should end WITH TWO BLANK LINES.
Outputs a song object as a JSON.
Press enter when each lyric starts, and when last lyric is done.
'''
TITLE = 'Short Song'
ARTIST = 'Anon'
FILE = 'songs/short_music.mp3'
LYRICS = 'songs/short_lyrics.txt'
DURATION = round(MP3(FILE).info.length)
# debug
JSON_FILENAME = FILE[FILE.find('/') + 1:FILE.find('.')]

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
    while True: # for debugging, while line_num < 5. When actually recording, make this infinite loop.
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
    wpm_list.append(0)
    reformatted_timestamps = [[t, l, w] for t, l, w in zip(timestamps, lyrics, wpm_list)] + [[DURATION, '', 0]]
    max_wpm = max(wpm_list)
    avg_wpm = sum(wpm_list) / sum(bool(l) for l in lyrics)
    with open('songs/' + JSON_FILENAME + '.json', 'w') as file:
        json.dump(obj=vars(Song(TITLE, ARTIST, DURATION, FILE, reformatted_timestamps, lyrics, max_wpm, avg_wpm)), fp=file)
    exit("Finished.")

def update_wpm(FILE: str):
    with open(FILE, 'r') as file:
        song = json.load(file,
                  object_hook=lambda dct: Song(dct['title'], dct['artist'], dct['duration'], dct['file'],
                                               dct['timestamps'], dct['lyrics'], dct['max_wpm'], dct['average_wpm']))
    maxwpm = 0
    nonempty_lyrics = 0
    sumwpm = 0
    for i in range(len(song.timestamps) - 1):
        song.timestamps[i][2] = 0 if not song.timestamps[i][1] else round(len(song.timestamps[i][1]) / 5 * 60 / (song.timestamps[i + 1][0] - song.timestamps[i][0]))
        sumwpm += song.timestamps[i][2]
        if song.timestamps[i][2] > maxwpm:
            maxwpm = song.timestamps[i][2]
        if bool(song.timestamps[i][1]):
            nonempty_lyrics += 1

    song.max_wpm = maxwpm
    song.average_wpm = round(sumwpm / nonempty_lyrics)
    with open(FILE, 'w') as file:
        json.dump(obj=vars(song), fp=file)


if __name__ == '__main__':
    #record()
    update_wpm('songs/json_files/bad_liar.json')
