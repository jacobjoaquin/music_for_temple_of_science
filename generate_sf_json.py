import os
import soundfile
import json

print('Generating Soundfile JSON file: soundsfiles.json')

file_path = './assets/'
files = os.listdir(file_path)
data = {}

for name in files:
    path_name = file_path + name
    sf = 0
    try:
        sf = soundfile.SoundFile(path_name)
        samplerate = sf.samplerate
        samples = len(sf)
        channels = sf.channels
        duration = samples / samplerate
        info = {
            'name': name,
            'path_name': path_name,
            'samples': samples,
            'samplerate': samplerate,
            'channels': channels,
            'duration': duration
        }

        data[name] = info
    except:
        pass

with open('soundfiles.json', 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)
