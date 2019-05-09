# LIBRARIES
import numpy as np                        # fundamental package for scientific computing
import pickle
import math
from matplotlib import pyplot as plt
from imprint_f import compute_imprint
from imprint_f import compute_position
from imprint_f import compute_imprint_global
print("Environment Ready")


# MAIN
# Parameters
f = open("imprint_base", "r")
p = pickle.load(f)
repertory = p[0]
window_w = p[1]
window_h = p[2]
step_downsample = p[3]  # Step for downsampling on LS
sigma = p[4]            # Amount of blur on LS
threshold = p[5]        # Threshold to compute LS
laser_position = p[6]
laser_pos_imp = laser_position - window_h[0]
delay_time = 0.2        # Time between each iteration
epsilon_time = 0.05

# Realsense camera parameter
len_im = p[7]
wid_im = p[8]
exp = p[9]
gain = p[10]
dis_shift = p[11]

# Imprint
window_imp = p[12]
step_imp = p[13]
imp_global = p[14]
base_imp = p[15]
size_imp = len(imp_global)

# Close parameters file
f.close()

# Imprint
#m = int(math.floor(window_h[1] - laser_position))
m = window_imp


f = open("imprints_1", "r")
p = pickle.load(f)
base_imp = p
f.close()

# Compute global imprint
step0 = 10
step1 = 2
step_imp = [10,2]

#pos = compute_position(imp_global, impC, m, step_imp, laser_pos_imp)
imp = base_imp[4]

size_imp = len(imp_global)
score_min = 1000000
i_min = -1

imp_global = imp_global.astype(np.int16)
imp = imp.astype(np.int16)

imp_win = imp[laser_pos_imp : laser_pos_imp + m]

for i in range (0, size_imp - m, step0):
    imp_g_win = imp_global[i : i + m]
    mask = np.abs(imp_g_win - imp_win)
    score = np.mean(mask)
    if score < score_min:
        imp_min = imp_g_win
        mask_min = mask
        score_min = score
        i_min = i
if i_min == -1:
    raise Exception('error : i_min not found')
k0 = i_min
k1 = i_min + step0   
k_min = i_min
for k in range (k0,k1,step1):
    imp_g_win = imp_global[k : k + m]
    mask = np.abs(imp_g_win - imp_win)
    score = np.mean(mask)
    if score < score_min:
        imp_min = imp_g_win
        mask_min = mask
        score_min = score
        k_min = k
pos = k_min

print(pos)

