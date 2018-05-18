import os
import soundfile
import json

print('Generating Soundfile JSON file: soundsfiles.json')

filename = 'soundfiles.json'
file_path = './assets/'
files = os.listdir(file_path)
data = {}
file_data = {}

# Load existing
with open(filename) as f:
    data = json.load(f)

# Get data from files
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

        file_data[name] = info
    except:
        pass

# Update existing
for k in file_data.keys():
    # Update from file
    for k2, v in file_data[k].items():
        data[k][k2] = v

# Save
with open(filename, 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)
