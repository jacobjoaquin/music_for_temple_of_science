import os
import soundfile
import json

print('Generating Soundfile JSON file: soundsfiles.json')

filename = 'soundfiles.json'
file_path = './assets/'
files = os.listdir(file_path)
data = {}
file_data = {}

# Default fields
default_fields = {
    'amp': 1
}

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
for name, fields in file_data.items():
    # Update from file
    for k, v in file_data[name].items():
        data[name][k] = v

# Add default if it doesn't exist in data
for name, fields in data.items():
    for k, v in default_fields.items():
        if k not in fields.keys():
            data[name][k] = v

# Save file
with open(filename, 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)
