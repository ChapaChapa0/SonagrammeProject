# LIBRARIES
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import time
import pyaudio
import wave
import audioop
import sys
import math
import pickle
from imprint_f import compute_imprint
from imprint_f import compute_position
print("Environment Ready")
    

# MAIN
# Parameters
f = open("imprint_base", "r")
p = pickle.load(f)
repertory = p[0]
window_w = p[1]
window_h = p[2]
step_downsample = p[3]  # Step for downsampling on LS
sigma = p[4]            # Amount of blur on LS
threshold = p[5]        # Threshold to compute LS
laser_position = p[6]
delay_time = 0.05        # Time between each iteration

# Realsense camera parameter
len_im = p[7]
wid_im = p[8]
exp = p[9]
gain = p[10]
dis_shift = p[11]

# Imprint
window_imp = p[12]
step_imp = p[13]
imprint_global = p[14]
size_imp = len(imprint_global)

# Close parameters file
f.close()

# INIT AUDIO
# Audio path
audio_path = repertory + 'empreintes_2.wav'

# Open the wav file in read-only mode
wave_file = wave.open(audio_path,"rb")
p = pyaudio.PyAudio()

# Audio parameters
file_format = p.get_format_from_width(wave_file.getsampwidth())
nb_channels = wave_file.getnchannels()
width = wave_file.getsampwidth()
framerate = wave_file.getframerate()
nb_frames = wave_file.getnframes()
time_wave = float(nb_frames) / float(framerate)
time_pixel = 0.01

# Open the data stream
stream = p.open(format = file_format,
                channels = nb_channels,
                rate = framerate,
                output = True)


# Init acceleration parameters
speed = 1.0
new_fr = framerate

# Init data flow block
chunk_size = int(math.ceil(framerate * delay_time))
data = "init"

# L_POS
l_pos = [0,0,0,0,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,130,140,150,
         160,170,180,190,200,210,220,230,240,250,252,254,256,258,260,262,264,266,268,270,272,274,276,278,280,
         285,290,295,300,305,310,315,320,325,330,335]
    
# Find imprint position on global imprint
start_pos = 0
pos = 0

# Lecture start when the sona start moving
epsilon = 2
i = 0
while (pos < start_pos + epsilon) and (pos > start_pos - epsilon):
    
    pos = l_pos[i]
    i += 1
    
#    print(str(i) + ' : ' + str(pos))
    
    # Pause
    time.sleep(delay_time)

# LOOP
old_pos = l_pos[i-1]
epsilon_time = 0.005
while len(l_pos[i:-1]) > 0:

    start = time.time()

    pos = l_pos[i]
    
    print(str(i) + ' : ' + str(pos))

    # Repeat last buffer if same imprint found
    if old_pos > pos + epsilon:
        speed = 1.0
        chunk_size = int(math.ceil(framerate * delay_time * speed))
    # Else continue lecture
    else:
        speed = ((pos - old_pos) * time_pixel) / delay_time
        chunk_size = int(math.ceil(framerate * delay_time * speed))
        data = wave_file.readframes(chunk_size)

    # Sleep
    end = time.time()
    computing_time = end - start
    if computing_time < delay_time:
        time.sleep(delay_time - computing_time - epsilon_time)

    # Play sound according to new speed
    new_fr = int(round(framerate / speed))
    modified_data = audioop.ratecv(data, width, nb_channels, framerate, new_fr, None)[0]
    stream.write(modified_data)
    
    old_pos = pos
    
    i += 1

# Close PyAudio
p.terminate()

# Close file stream
wave_file.close()