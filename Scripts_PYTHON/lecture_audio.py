# Libraries
import pyaudio
import wave
import audioop
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

# Acceleration parameters
speed = 1
new_fr = framerate
i = 0

#Read data
data = wave_file.readframes(chunk_size)
stream.write(data)

# Play
while len(data) > 0:
    if i < 60:
        speed = 0.99
    else:
        speed = 1.02
    new_fr = int(round(new_fr / speed))
    data = wave_file.readframes(chunk_size)
    modified_data = audioop.ratecv(data, width, nb_channels, framerate, new_fr, None)[0]
    stream.write(modified_data)
    i += 1

# Stop data flow
stream.stop_stream()
stream.close()

# Close PyAudio
p.terminate()