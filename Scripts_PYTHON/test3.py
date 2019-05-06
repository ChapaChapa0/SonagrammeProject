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


f = open("imprints0", "r")
p = pickle.load(f)
imp_global = p[0]
base_imprint = p[1]
f.close()

# Compute imprint
impA = base_imprint[0]
impB = base_imprint[1]
impC = base_imprint[2]
impD = base_imprint[3]
impE = base_imprint[4]

# Compute global imprint
step0 = 10
step1 = 2
step_imp = [10,2]

#pos = compute_position(imp_global, impC, m, step_imp, laser_pos_imp)
imp = impD

size_imp = len(imp_global)
score_min = 1000000
i_min = -1
imp_win = imp[laser_pos_imp - m : laser_pos_imp + m]

for i in range (m, size_imp - m, step0):
    imp_g_win = imp_global[i - m : i + m]
    mask1 = np.abs(imp_g_win - imp_win)
    mask2 = np.abs(imp_win - imp_g_win)
    score = np.mean(mask1) + np.mean(mask2)
    if score < score_min:
        score_min = score
        i_min = i
if i_min == -1:
    raise Exception('error : i_min not found')
k0 = i_min
k1 = i_min + step0   
k_min = i_min
for k in range (k0,k1,step1):
    imp_g_win = imp_global[k - m : k + m]
    mask1 = np.abs(imp_g_win - imp_win)
    mask2 = np.abs(imp_win - imp_g_win)
    score = np.mean(mask1) + np.mean(mask2)
    if score < score_min:
        score_min = score
        k_min = k
pos = k_min
