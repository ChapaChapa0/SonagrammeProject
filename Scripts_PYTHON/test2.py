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
search_win = p[14]
imprint_global = p[15]
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

l_pos_2 = [0,0,0,0,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,130,140,150,
         160,170,180,190,200,210,220,230,240,250,252,250,245,240,235,230,225,220,215,210,205,200,195,190,185,
         170,160,150,140,130,120,118,116,114,112,110]
    
# Find imprint position on global imprint
start_pos = 0
pos = 0

# Lecture start when the sona start moving
epsilon = 2
i = 0
while (pos < start_pos + epsilon) and (pos > start_pos - epsilon):
    
    pos = l_pos_2[i]
    i += 1
    
#    print(str(i) + ' : ' + str(pos))
    
    # Pause
    time.sleep(delay_time)

# LOOP
pre_pos = l_pos_2[i-1]
epsilon_time = 0.005
while i < len(l_pos) and len(data) > 0:

    start = time.time()

    pos = l_pos_2[i]
    
#    print(str(i) + ' : ' + str(pos))

    # Deduce if lecture is over
    if pos > 320:
        data = ""
    # Else continue lecture
    else:
        # If same position nothing is readen
        if pos == pre_pos:
            modified_data = ''
        else:
            # Determine speed of lecture and chunk_size according to this speed
            speed = abs(((pre_pos - pos) * time_pixel) / delay_time)
            chunk_size = int(math.ceil(framerate * delay_time * speed))
            
            # Determine position in lecture
            if pos < pre_pos:
                sound_pos = int(round(pos * time_pixel * framerate - chunk_size))
                wave_file.setpos(sound_pos)
                data = wave_file.readframes(chunk_size)
                data = audioop.reverse(data, width)
            else:
                sound_pos = int(round(pos * time_pixel * framerate))
                wave_file.setpos(sound_pos)
                data = wave_file.readframes(chunk_size)
        
            # Determine new framerate according to new speed
            new_fr = int(round(framerate / speed))
            modified_data = audioop.ratecv(data, width, nb_channels, framerate, new_fr, None)[0]
    
            # Rewind wave file for next iteration
            wave_file.rewind()
    
        # Sleep before next iteration
        end = time.time()
        computing_time = end - start
        if computing_time < delay_time:
            time.sleep(delay_time - computing_time - epsilon_time)

        # Play sound with new framerate
        stream.write(modified_data)

        pre_pos = pos
        i += 1

# Close PyAudio
p.terminate()

# Close file stream
wave_file.close()