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

# LOOP
condition = True
iteration = 0
old_i = 0
LS_base = []
while iteration < 5:
    raw_input("Press enter...")
    
    for i in range (0,5):
        frameset = pipe.wait_for_frames()

    # Get arrays of color data
    color_frame = frameset.get_color()  
    color = np.asanyarray(color_frame.get_data())
    
    if True:
        # Get arrays of depth data
        depth_frame = frameset.get_depth_frame()
        depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)
    
        depth0 = np.transpose(depth[window_h[0]: window_h[1]])
        depth0 = np.transpose(depth0[window_w[0]:window_w[1]])

        LS = calcul_LS(depth0)
        LS_base.append(LS)
    
        iteration = iteration + 1
    else:
        condition = False


pipe.stop()


#config = {'len_im', 'wid_im', 'window_w', 'window_h', 'nb_bandes', 'exp', 'gain'}
#p=open("slices_base", "w") # le fichier de sauvegarde s'appelle “f”
#pickle.dump(config, p)
#p.close()
    
    
    
    