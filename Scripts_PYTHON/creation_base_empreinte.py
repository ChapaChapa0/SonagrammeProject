# LIBRARIES
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import time
import wave
import math
import sys
import pickle
from empreinte_f import calcul_empreinte
from empreinte_f import calcul_empreinte_global
print("Environment Ready")


# MAIN
# Parameters
repertory = "C:\\Users\\Hatem\\Documents\\Paul\\SonagrammeProject\\Scripts_PYTHON\\Audio\\"
window_w = [260,390]
window_h = [100, 480]
step_downsample = 2  # Step for downsampling on LS
sigma = 5            # Amount of blur on LS
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
            emit = sens.get_option(rs.option.emitter_enabled) # Get emitter status
            sens.set_option(rs.option.exposure, exp) # Set exposure
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
base_empreinte = []
while iteration < 5:

    raw_input("Press enter...")
    
    frameset = pipe.wait_for_frames()

    # Get arrays of depth data
    depth_frame = frameset.get_depth_frame()
    depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)

    # Compute LS
    depth0 = np.transpose(depth[window_h[0]: window_h[1]])
    depth0 = np.transpose(depth0[window_w[0]:window_w[1]])
    empreinte = calcul_empreinte(depth0, step_downsample, sigma, threshold)
    base_empreinte.append(empreinte)

    iteration = iteration + 1
    
# Calcul empreinte global
empreinte_global = calcul_empreinte_global(base_empreinte, step_downsample, sigma, threshold)

# Close streaming pipe
pipe.stop()

# Save configuration for lecture
config = [repertory, window_w, window_h, step_downsample, sigma, threshold,
          len_im, wid_im, exp,gain, dis_shift, empreinte_global]
f = open("slices_base", "w")
pickle.dump(config, f)
f.close()
    
    
    
    