#!/usr/bin/python
"""Temple of Science"""

import json
from csd.pysco import PythonScoreBin
from random import random
from random import choice
from random import seed
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

    score.i(instr_reverb, 0, dur, amp, delay_left, delay_right, room_size, damp)

def reverb_mono(dur, amp, delay_left, delay_right, room_size, damp):
    '''Interface for Csound orchesta reverb instrument.'''

    score.i(instr_reverb_mono, 0, dur, amp, delay_left, delay_right, room_size, damp)

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

def generate_random_sequence():
    keys = soundfiles.keys()
    sequence = []
    for name in keys:
        sequence.append([name, 1])
        sequence.append([name, -1])
    shuffle(sequence)
    return sequence


score = PythonScoreBin()
cue = score.cue

# instruments
instr_mono_player = 1
instr_stereo_player = 2
instr_reverb = 100
instr_reverb_mono = 101

# Load soundfile data
json_soundfiles = open('soundfiles.json')
soundfiles = json.loads(json_soundfiles.read())
score_length = calculate_runtime()

# About
info()

# Begin Score
seed(0)

reverb(score_length + 4, 0.75, 0.0223, 0.0213, 0.705, 0.695)
reverb_mono(score_length + 4, 0.75, 0.0423, 0.0413, 0.705, 0.695)

seq0 = generate_random_sequence() + generate_random_sequence()
seq1 = generate_random_sequence() + generate_random_sequence()

t = 0
for sf in seq0:
    with cue(t):
        t += play_sample(sf[0], pch=sf[1], mix=0.65)

t = 0
for sf in seq1:
    with cue(t):
        t += play_sample(sf[0], pch=sf[1], mix=0.25)
