#!/usr/bin/python
"""Temple of Science"""

import json
from csd.pysco import PythonScoreBin
from random import random
from random import choice
from random import shuffle
from random import uniform

def info():
    print "\033[0;31m" + ('=' * 72) + "\033[1;33m"
    print __doc__
    print_runtime()
    print "\033[0;31m" + ('=' * 72) + "\033[0m"

def calculate_runtime():
    total_time = 0
    for key, sf in soundfiles.iteritems():
        total_time += sf['duration']
    return total_time

def print_runtime():
    print("Estimated Runtime: " + str(calculate_runtime() / 60))

def pf_filename(f):
    return '"' + f + '"'

def sampler(sf, start_time, dur, pch=1, mix=1):
    amp = sf['amp']

    if sf['channels'] == 1:
        mono_player(sf['path_name'], start_time, dur, amp, pch=pch, mix=mix)
    elif sf['channels'] == 2:
        stereo_player(sf['path_name'], start_time, dur, amp, pch=pch, mix=mix)
    else:
        print("WARNING: channels for sound file is not 1 or 2")

def mono_player(filename, start_time, dur, amp=1, pch=1, mix=1):
    '''Plays a mono sample'''

    score.i(instr_mono_player, 0, dur, amp, pch, pf_filename(filename), start_time, mix)

def stereo_player(filename, start_time, dur, amp=1, pch=1, mix=1):
    '''Plays a stereo sample'''

    score.i(instr_stereo_player, 0, dur, amp, pch, pf_filename(filename), start_time, mix)


def reverb(dur, amp, delay_left, delay_right, room_size, damp):
    '''Interface for Csound orchesta reverb instrument.'''

    # score.i(instr_reverb, 0, dur, amp, delay_left, delay_right, room_size, damp)
    # Swap left and right
    score.i(instr_reverb, 0, dur, amp, delay_right, delay_left, room_size, damp)

def random_sampler():
    sf = soundfiles[choice(soundfiles.keys())]
    dur = sf['duration'] * random()
    start_time = random() * (sf['duration'] - dur)
    mix = random()
    sampler(sf, start_time, dur, mix)
    return dur

def play_sample(name, pch=1, mix=1):
    sf = soundfiles[name]
    dur = sf['duration']
    start_time = 0
    sampler(sf, start_time, dur, pch=pch, mix=mix)
    return dur

score = PythonScoreBin()
cue = score.cue

# instruments
instr_mono_player = 1
instr_stereo_player = 2
instr_reverb = 100

# Load soundfile data
json_soundfiles = open('soundfiles.json')
soundfiles = json.loads(json_soundfiles.read())
score_length = calculate_runtime()

# About
info()

# Begin Score
reverb(score_length + 4, 2.333, 0.0223, 0.0213, 0.4, 0.3)

# Shuffle two sides
L0 = soundfiles.keys()
L1 = soundfiles.keys()
shuffle(L0)
shuffle(L1)

t = 0
for sf in L0:
    with cue(t):
        t += play_sample(sf, pch=1, mix=0.8)

t = 0
for sf in L1:
    with cue(t):
        t += play_sample(sf, pch=-1, mix=0.25)
