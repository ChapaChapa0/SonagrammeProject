# LIBRARIES
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import time
import wave
import math
import sys
import pickle
from LS_f import calcul_LS
print("Environment Ready")


# MAIN
# Parameters
repertory = "C:\\Users\\Hatem\\Documents\\Paul\\SonagrammeProject\\Scripts_PYTHON\\Audio\\"
window_w = [260,390]
window_h = [100, 480]
step_downsample = 2  # Step for downsampling on LS
sigma = 1.5          # Amount of blur on LS
threshold = 550      # Threshold to compute LS

# Realsense camera parameter
len_im = 640
wid_im = 480
exp = 8000
gain = 16
dis_shift = 0

# INIT
# Adjust exposure and gain
ctx = rs.context()
devices = ctx.query_devices()
for dev in devices:
    advnc_mode = rs.rs400_advanced_mode(dev)
    depth_table_control_group = advnc_mode.get_depth_table()
    depth_table_control_group.disparityShift = dis_shift
    advnc_mode.set_depth_table(depth_table_control_group)
    sensors = dev.query_sensors();
    for sens in sensors:
        if sens.is_depth_sensor():
            emit = sens.get_option(rs.option.emitter_enabled); # Get emitter status
            sens.set_option(rs.option.exposure, exp); # Set exposure
            sens.set_option(rs.option.gain, gain) # Set gain


pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, len_im, wid_im, rs.format.rgb8, 30) #1280 * 720 ou 640 * 480
config.enable_stream(rs.stream.depth, len_im, wid_im, rs.format.z16, 30) #1280 * 720 ou 640 * 480
profile = pipe.start(config)

# Discard first frames
for i in range (0,5):
    frameset = pipe.wait_for_frames()

# LOOP
iteration = 0
old_i = 0
LS_base = []
while iteration < 30:
    
    raw_input("Press enter...")
    
    frameset = pipe.wait_for_frames()

    # Get arrays of depth data
    depth_frame = frameset.get_depth_frame()
    depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)

    # Compute LS
    depth0 = np.transpose(depth[window_h[0]: window_h[1]])
    depth0 = np.transpose(depth0[window_w[0]:window_w[1]])
    LS = calcul_LS(depth0, step_downsample, sigma, threshold)
    LS_base.append(LS)
    
    iteration = iteration + 1

AS_base = []
AE_base = []
audio_path = repertory + 'empreintes.wav'

# Open the wav file in read-only mode
signal = wave.open(audio_path,"rb")

# Audio parameters
nb_channels = signal.getnchannels()
width = signal.getsampwidth()
framerate = signal.getframerate()

nb_LS = len(LS_base)
size_slice = math.floor(len(signal) / (nb_LS - 1))


for i in range (0,len(LS_base)):
    
    # Save slice file
    slice_signal = signal[i * size_slice : -1]
    slice_path = repertory + 'Slices\\slice' + str(i) + '.wav'
    AS_base.append(slice_path)
    slice_file = wave.open(slice_path, 'wb')
    slice_file.setnchannels(nb_channels)
    slice_file.setsampwidth(width)
    slice_file.setframerate(framerate)
    slice_file.writeframes(slice_signal)
    slice_file.close()
    
    # Save slice file in reverse
    ecils_signal = signal[0 : i * size_slice].reverse
    ecils_path = repertory + 'Secils\\ecils' + str(i) + '.wav'
    AE_base.append(ecils_path)
    ecils_file = wave.open(ecils_path, 'wb')
    ecils_file.setnchannels(nb_channels)
    ecils_file.setsampwidth(width)
    ecils_file.setframerate(framerate)
    ecils_file.writeframes(ecils_signal)
    ecils_file.close()


# Close signal stream
signal.close()

# Close streaming pipe
pipe.stop()

# Save configuration for lecture
config = [repertory, window_w, window_h, step_downsample, sigma, threshold,
          len_im, wid_im, exp,gain, dis_shift, LS_base, AS_base, AE_base]
f = open("slices_base", "w")
pickle.dump(config, f)
f.close()
    
    
    
    