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
from matplotlib import pyplot as plt
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
laser_pos_imp = laser_position - window_h[0]
delay_time = 0.1        # Time between each iteration
epsilon_time = 0.01

# Realsense camera parameter
len_im = p[7]
wid_im = p[8]
exp = p[9]
gain = p[10]
dis_shift = p[11]

# Other parameters
window_imp = p[12]
#step_imp = p[13]
step_imp = 1
search_win = p[14]
imprint_global = p[15]
size_imp = len(imprint_global)

# Close parameters file
f.close()


# INIT CAMERA
# Adjust exposure and gain
ctx = rs.context()
devices = ctx.query_devices()
for dev in devices:
    sensors = dev.query_sensors();
    for sens in sensors:
        if sens.is_depth_sensor():
            emit = sens.get_option(rs.option.emitter_enabled); # Get emitter status
            sens.set_option(rs.option.exposure, exp); # Set exposure
            sens.set_option(rs.option.gain, gain) # Set gain
            sens.set_option(rs.option.emitter_enabled, dis_shift) # Disable emitter
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, len_im, wid_im, rs.format.rgb8, 30) #1280 * 720 ou 640 * 480
config.enable_stream(rs.stream.depth, len_im, wid_im, rs.format.z16, 30) #1280 * 720 ou 640 * 480
profile = pipe.start(config)

# Discard first frames
for i in range (0,5):
    frameset = pipe.wait_for_frames()

# INIT AUDIO
# Audio path
audio_path = repertory + 'empreintes_3.wav'

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
time_pixel = time_wave / size_imp

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

# Get new frames
frameset = pipe.wait_for_frames()

# Get arrays of depth data
depth_frame = frameset.get_depth_frame()
depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)

# Compute imprint
imprint = compute_imprint(depth, window_h, window_w, step_downsample, sigma, threshold)

# Find imprint position on global imprint
start_pos = 0
search_win_init = size_imp - window_imp
pos = compute_position(imprint_global, imprint, window_imp, step_imp, laser_pos_imp, start_pos, search_win_init)
start_pos = pos
pre_pos = pos

# Lecture start when the sona start moving
epsilon = 3
while (pos < start_pos + epsilon) and (pos > start_pos - epsilon):
    
    # Get new frames
    frameset = pipe.wait_for_frames()
    
    # Get arrays of depth data
    depth_frame = frameset.get_depth_frame()
    depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)
    
    # Compute imprint
    imprint = compute_imprint(depth, window_h, window_w, step_downsample, sigma, threshold)
        
    # Find imprint position on global imprint
    pre_pos = pos
    pos = compute_position(imprint_global, imprint, window_imp, step_imp, laser_pos_imp, pre_pos, search_win)
    
    # Pause
    time.sleep(delay_time)

# LOOP
reverse = (pos < start_pos)
while len(data) > 0:

    start = time.time()
    
    # Get new frames
    frameset = pipe.wait_for_frames()

    # Get arrays of depth data
    depth_frame = frameset.get_depth_frame()
    depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)

    # Compute imprint
    imprint = compute_imprint(depth, window_h, window_w, step_downsample, sigma, threshold)
        
    # Find imprint position on global imprint
    pos = compute_position(imprint_global, imprint, window_imp, step_imp, laser_pos_imp, pre_pos, search_win)
    
    # Deduce if lecture is over
    if (pos > size_imp - 10 and not reverse) or (pos < 10 and reverse):
        data = ''
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
                # Audio is in reverse if lecture goes backward
                sound_pos = int(round(pre_pos * time_pixel * framerate - chunk_size))
                if sound_pos < 0:
                    wave_file.setpos(0)
                else:
                    wave_file.setpos(sound_pos)
                data = wave_file.readframes(chunk_size)
                data = audioop.reverse(data, width)
                reverse = True
            else:
                sound_pos = int(round(pre_pos * time_pixel * framerate))
                wave_file.setpos(sound_pos)
                data = wave_file.readframes(chunk_size)
                reverse = False
        
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
    
# Stop data flow
stream.stop_stream()
stream.close()

# Close PyAudio
p.terminate()

# Close file stream
wave_file.close()

# Close streaming pipe
pipe.stop()