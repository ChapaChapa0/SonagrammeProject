# LIBRARIES
import numpy as np                        # fundamental package for scientific computing
import pickle
from matplotlib import pyplot as plt
from imprint_f import compute_imprint
from imprint_f import compute_position
from imprint_f import compute_imprint_global
print("Environment Ready")


# MAIN
# Parameters
repertory = "C:\\Users\\Hatem\\Documents\\Paul\\SonagrammeProject\\Scripts_PYTHON\\Audio\\"
window_w = [260,390]
window_h = [100, 340]
step_downsample = 2  # Step for downsampling on imprint
sigma = 5            # Amount of blur on imprint
threshold = 560      # Threshold to compute imprint
laser_position = 220
laser_pos_imp = laser_position - window_h[0]

# Realsense camera parameter
len_im = 640
wid_im = 480
exp = 8000
gain = 16
dis_shift = 0

# Imprint
m = 100
step_imp = [10,2]


f = open("base_depth", "r")
base_depth = pickle.load(f)
depth0 = base_depth[0]
depth1 = base_depth[1]
depth2 = base_depth[2]
f.close()

# Compute imprint
impA = compute_imprint(depth0, window_h, window_w, step_downsample, sigma, threshold)

impB = compute_imprint(depth1, window_h, window_w, step_downsample, sigma, threshold)

impC = compute_imprint(depth2, window_h, window_w, step_downsample, sigma, threshold)

# Compute global imprint
step0 = 10
step1 = 2


imp0 = impA
size_imp = len(imp0)
score_min = 1000000
imp0_win_min = []
i_min = -1

# impB
imp = impB
imp_win = impB[0:m]

for i in range (0, size_imp - m, step0):
    imp0_win = imp0[i : i + m]
    mask1 = np.abs(imp_win - imp0_win)
    mask2 = np.abs(imp0_win - imp_win)
    score = np.mean(mask1) + np.mean(mask2)
    if score < score_min:
        score_min = score
        i_min = i
        imp0_win_min = imp0_win
if i_min == -1:
    raise Exception('error : i_min not found')
elif i_min + step0 > size_imp:
    k1 = size_imp
else:
    k1 = i_min + step0
k0 = i_min
k_min = i_min
for k in range (k0, k1, step1):
    imp0_win = imp0[k : k + m]
    mask1 = np.abs(imp_win - imp0_win)
    mask2 = np.abs(imp0_win - imp_win)
    score = np.mean(mask1) + np.mean(mask2)
    if score < score_min:
        score_min = score
        k_min = k
        imp0_win_min = imp0_win
imp0 = np.concatenate((imp0, imp[size_imp - k_min - 1 : -1]), axis = 0)

# impC
imp = impC
imp_win = impC[0:m]

# Reset score and min
score_min = 1000000
imp0_win_min = []
i_min = -1

for i in range (0, size_imp - m, step0):
    imp0_win = imp0[i : i + m]
    mask1 = np.abs(imp_win - imp0_win)
    mask2 = np.abs(imp0_win - imp_win)
    score = np.mean(mask1) + np.mean(mask2)
    if score < score_min:
        score_min = score
        i_min = i
        imp0_win_min = imp0_win
if i_min == -1:
    raise Exception('error : i_min not found')
elif i_min + step0 > size_imp:
    k1 = size_imp
else:
    k1 = i_min + step0
k0 = i_min
k_min = i_min
for k in range (k0, k1, step1):
    imp0_win = imp0[k : k + m]
    mask1 = np.abs(imp_win - imp0_win)
    mask2 = np.abs(imp0_win - imp_win)
    score = np.mean(mask1) + np.mean(mask2)
    if score < score_min:
        score_min = score
        k_min = k
        imp0_win_min = imp0_win
imp0 = np.concatenate((imp0, imp[size_imp - k_min - 1 : -1]), axis = 0)

imp_global = imp0

pos = compute_position(imp_global, impA, m, step_imp, laser_pos_imp)

