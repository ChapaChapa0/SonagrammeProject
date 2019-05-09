# LIBRARIES
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import sys
import pickle
from matplotlib import pyplot as plt
from imprint_f import compute_imprint
from imprint_f import compute_imprint_global
print("Environment Ready")


# MAIN
# Parameters
repertory = "C:\\Users\\Hatem\\Documents\\Paul\\SonagrammeProject\\Scripts_PYTHON\\Audio\\"
window_w = [260,390]
window_h = [110, 330]
step_downsample = 2  # Step for downsampling on imprint
sigma = 5            # Amount of blur on imprint
threshold = 560      # Threshold to compute imprint
laser_position = 220
laser_pos_imp = laser_position - window_h[1]

# Realsense camera parameter
len_im = 640
wid_im = 480
exp = 8000
gain = 16
dis_shift = 0

# Imprint
window_imp = 80
step_imp = 2

# INIT
# Adjust exposure and gain()
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
nb_frames = 5
base_imprint = []
l_color = []
while iteration < 3:

    raw_input("Press enter...")
    
    imprint_m = 0
    for i in range (0,nb_frames):
        frameset = pipe.wait_for_frames()

        # Get arrays of depth data
        depth_frame = frameset.get_depth_frame()
        depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)

        # Compute imprint
        imprint = compute_imprint(depth, window_h, window_w, step_downsample, sigma, threshold)
        
        # Compute mean of imprint
        imprint_m += imprint

    # Add imprint to the base
    imprint_m = imprint_m/nb_frames
    base_imprint.append(imprint_m)

    # Color
    color_frame = frameset.get_color_frame()
    color = np.asanyarray(color_frame.get_data())
    color = color[window_h[0] : window_h[1]]
    l_color.append(color)

    iteration = iteration + 1

# Calcul imprint global
imprint_global = compute_imprint_global(base_imprint, window_imp, step_imp, laser_pos_imp)

# Close streaming pipe
pipe.stop()

# Save configuration for lecture
config = [repertory, window_w, window_h, step_downsample, sigma, threshold, laser_position,
          len_im, wid_im, exp, gain, dis_shift, window_imp, step_imp, imprint_global, base_imprint]
f = open("imprint_base", "w")
pickle.dump(config, f)
f.close()



    