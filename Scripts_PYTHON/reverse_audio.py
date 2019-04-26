# Libraries
import pyaudio
import wave
import sys

# Data flow block
chunk_size = 1024

# Open the wav file in read-only mode
wave_file = wave.open('C:\Users\Hatem\Documents\Paul\SonagrammeProject\Scripts_MATLAB\Audio\empreintes_2.wav',"rb")
p = pyaudio.PyAudio()

# Audio parameters
file_format = p.get_format_from_width(wave_file.getsampwidth())
nb_channels = wave_file.getnchannels()
width = wave_file.getsampwidth()
framerate = wave_file.getframerate()

# Open the data stream
stream = p.open(format = file_format,
                channels = nb_channels,
                rate = framerate,
                output = True)

full_data = []
data = wave_file.readframes(1024)

while data:    
    full_data.append(data)
    data = wave_file.readframes(1024)

data = ''.join(full_data)[::-1]

for i in range(0, len(data), 1024):
    stream.write(data[i:i+1024])

# Stop data flow
stream.stop_stream()
stream.close()

# Close PyAudio
p.terminate()