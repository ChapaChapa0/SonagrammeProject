import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
#import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import open3d as op                       # 3d data processing library
import time
from sklearn.cluster import KMeans        # kmeans method for filtering
from PIL import Image
print("Environment Ready")

# MAIN
# Parameters
len_im = 640
wid_im = 480
exp = 8000
gain = 16

# INIT
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

# LOOP
condition = True
while condition:
    raw_input("Press enter...")
    
    for i in range (0,5):
        frameset = pipe.wait_for_frames()
    color_frame = frameset.get_color_frame()
    depth_frame = frameset.get_depth_frame()

    # On recupere les donnees sous forme de tableau
    color = np.asanyarray(color_frame.get_data())
    depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)
    
    condition = False

# Cleanup:
pipe.stop()