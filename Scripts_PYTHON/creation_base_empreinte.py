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
window_h = [100, 480]
step_downsample = 2  # Step for downsampling on imprint
sigma = 5            # Amount of blur on imprint
threshold = 550      # Threshold to compute imprint

# Realsense camera parameter
len_im = 640
wid_im = 480
exp = 8000
gain = 16
dis_shift = 0

# Imprint
window_imp = 100
step_imp = [20,5]

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
base_imprint = []
while iteration < 1:

    raw_input("Press enter...")
    
    frameset = pipe.wait_for_frames()

    # Get arrays of depth data
    depth_frame = frameset.get_depth_frame()
    depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)

    # Compute LS
    depth0 = np.transpose(depth[window_h[0]: window_h[1]])
    depth0 = np.transpose(depth0[window_w[0]:window_w[1]])
    imprint = compute_imprint(depth0, step_downsample, sigma, threshold)
    base_imprint.append(imprint)

    iteration = iteration + 1
    
# Calcul imprint global
imprint_global = compute_imprint_global(base_imprint, window_imp, step_imp)

# Close streaming pipe
pipe.stop()

# Save configuration for lecture
config = [repertory, window_w, window_h, step_downsample, sigma, threshold, len_im,
          wid_im, exp, gain, dis_shift, window_imp, step_imp, imprint_global]
f = open("slices_base", "w")
pickle.dump(config, f)
f.close()
    
    
    
    