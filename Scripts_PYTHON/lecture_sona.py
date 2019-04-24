# LIBRARIES
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import open3d as op                       # 3d data processing library
import time
import pyaudio
import wave
import audioop
import sys
print("Environment Ready")

# FUNCTIONS
def calcul_LS(depth0):
    
    epsilon = 0.001
    LS = depth0[0:-1:2][0:-1:2]
    condition1 = np.where(depth0 > 550)
    
# MAIN
# Parameters
len_im = 640
wid_im = 480
window_w = [261,390]
window_h = [101, 480]

# Realsense camera parameter
exp = 8000
gain = 16
dis_shift = 0;

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

# INIT AUDIO
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

# Read data
data = wave_file.readframes(chunk_size)
stream.write(data)

# LOOP
condition = True
iteration = 0
while iteration < 20:
    raw_input("Press enter...")
    
    # Get new frames
    frameset = pipe.wait_for_frames()

    # Get arrays of color data
    color_frame = frameset.get_color_frame()
    color = np.asanyarray(color_frame.get_data())
    
    if True:
        # Get arrays of depth data
        depth_frame = frameset.get_depth_frame()
        depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)
        
        depth0 = np.transpose(depth[window_h[0]: window_h[1]])
        depth0 = np.transpose(depth0[window_w[0]:window_w[1]])

        
        # Play sound according to new speed
        new_fr = int(round(new_fr / speed))
        data = wave_file.readframes(chunk_size)
        modified_data = audioop.ratecv(data, width, nb_channels, framerate, new_fr, None)[0]
        stream.write(modified_data)
    
        iteration += 1
    else:
        condition = False
    
# Stop data flow
stream.stop_stream()
stream.close()

# Close PyAudio
p.terminate()

# Close streaming pipe
pipe.stop()