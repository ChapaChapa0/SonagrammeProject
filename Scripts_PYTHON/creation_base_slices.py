import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
#import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import open3d as op                       # 3d data processing library
import time
from sklearn.cluster import KMeans        # kmeans method for filtering
from PIL import Image
print("Environment Ready")

def calcul_LS(depth0):
    
    epsilon = 0.001
    LS = depth0[0:-1:2][0:-1:2]
    condition1 = np.where(depth0 > 550)
    
    for i in range (1:len(condition1)):
        condition1[i]
    return LS

# MAIN
# Parameters
len_im = 640
wid_im = 480
window_w = [261,390]
window_h = [101, 480]
nb_bandes = 10
nb_bandes = 10

# Realsense camera parameter
exp = 8000
gain = 16
dis_shift = 0;

# Compute parameters for LS
nb_rows_S = window_w[1] - window_w[0]
nb_columns_S = window_h[1] - window_h[0]
valeurs_f_S = np.arange(nb_rows_S)
valeurs_t = np.arange(nb_columns_S)
partition = np.floor(np.linspace(0,nb_rows_S,nb_bandes+1)).astype(int)

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
    color_frame = fram    
    # On recupere les donnees sous forme de tableau
    color = np.asanyarray(color_frame.get_data())
eset.get_color_frame()
    depth_frame = frameset.get_depth_frame()
    
    if True:
        depth = np.asanyarray(depth_frame.get_data()).astype(np.uint16)
    
        depth0 = np.transpose(depth[window_h[0]: window_h[1]])
        depth0 = np.transpose(depth0[window_w[0]:window_w[1]])

        LS = calcul_LS(depth0)
        LS_base.append(LS)
    
        iteration = iteration + 1
    else:
        condition = False


pipe.stop()

# On repasse au format image
#color_raw = op.Image(color)
#depth_raw = op.Image(depth)

# Create pointcloud from the filtered depth and color image
#rgbd_image = op.create_rgbd_image_from_color_and_depth(color_raw, depth_raw);
#pcd = op.create_point_cloud_from_rgbd_image(rgbd_image ,op.PinholeCameraIntrinsic(
#        op.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
#pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
#op.draw_geometries([pcd])
    
#config = {'len_im', 'wid_im', 'window_w', 'window_h', 'nb_bandes', 'exp', 'gain'}
#p=open("slices_base", "w") # le fichier de sauvegarde s'appelle “f”
#pickle.dump(config, p)
#p.close()
    
    
    
    