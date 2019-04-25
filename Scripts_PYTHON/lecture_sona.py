# LIBRARIES
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import time
import pyaudio
import wave
import audioop
import sys
import math
from threading import Thread
print("Environment Ready")

# FUNCTIONS
def calcul_LS(depth0, step, sigma, seuil):
    
    LS = depth0[0:-1:step][0:-1:step]
    condition = np.where(LS > threshold)
    LS[condition] = 0
    return LS

def compare_LS(LS_base, LS0):
    i_min = 0
    score_min = 10000
    for i in range(0,len(LS_base)):
        LS = LS_base[i]
        masque = np.abs(LS - LS0)
        score = np.mean(masque)
        if score < score_min:
            score_min = score
            i_min = i
    return [i_min,score_min]
        

# MAIN
# Parameters
window_w = [260,390]
window_h = [100, 480]
step = 2         # Amount of downsampling on LS
sigma = 1.5      # Amount of blureness on LS
threshold = 550  # Seuil for LS computing
delay_time = 0.2 # Time between each iteration

# Realsense camera parameter
len_im = 640
wid_im = 480
exp = 8000
gain = 16
dis_shift = 0

# INIT CAMERA
# Parameters
len_im = 640
wid_im = 480
exp = 8000
gain = 16

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
            sens.set_option(rs.option.emitter_enabled, 0) # Disable emitter
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
audio_path = 'C:\Users\Hatem\Documents\Paul\SonagrammeProject\Scripts_MATLAB\Audio\empreintes_2.wav'

# Open the wav file in read-only mode
wave_file = wave.open(audio_path,"rb")
p = pyaudio.PyAudio()

# Audio parameters
file_format = p.get_format_from_width(wave_file.getsampwidth())
nb_channels = wave_file.getnchannels()
width = wave_file.getsampwidth()
framerate = wave_file.getframerate()
nb_frames = wave_file.getnframes()
duree_son = float(nb_frames) / float(framerate)
duree_LS = duree_son / (len(LS_base) - 1)

# Init data flow block
chunk_size = int(math.ceil(framerate * delay_time))

# Open the data stream
stream = p.open(format = file_format,
                channels = nb_channels,
                rate = framerate,
                output = True)

raw_input("Press enter...")
time.sleep(2)

# Read data
data = wave_file.readframes(chunk_size)
stream.write(data)

# Init acceleration parameters
speed = 1
new_fr = framerate

# LOOP
iteration = 0
old_i = 0

while len(data) > 0:
    
    start = time.time()
    
    # Get new frames
    frameset = pipe.wait_for_frames()

    # Get arrays of depth data
    depth_frame = frameset.get_depth_frame()
    depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)
        
    # Compute LS
    depth0 = np.transpose(depth[window_h[0]: window_h[1]])
    depth0 = np.transpose(depth0[window_w[0]:window_w[1]])
    LS = calcul_LS(depth0, step, sigma, threshold)
        
    # Compare LS with our base of LS
    res = compare_LS(LS_base, LS)
    i_min = res[0]
    score_min = res[1]
        
    # Deduce new speed and chunk_size from LS
    if old_i < i_min:
        speed = ((i_min - old_i) * duree_LS) / delay_time
        chunk_size = int(math.ceil(framerate * delay_time * speed))
        data = wave_file.readframes(chunk_size)
    else:
        speed = 1
        chunk_size = int(math.ceil(framerate * delay_time * speed))
        if i_min == (len(LS_base)-1):
            data = ""

    # Sleep
    end = time.time()
    computing_time = start - end
    if computing_time < delay_time:
        time.sleep(delay_time - computing_time)

    # Play sound according to new speed
    new_fr = int(round(framerate / speed))
    modified_data = audioop.ratecv(data, width, nb_channels, framerate, new_fr, None)[0]
    stream.write(modified_data)
    
    old_i = i_min
    iteration += 1
    
# Stop data flow
stream.stop_stream()
stream.close()

# Close PyAudio
p.terminate()

# Close streaming pipe
pipe.stop()