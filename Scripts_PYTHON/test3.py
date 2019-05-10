# LIBRARIES
import numpy as np                        # fundamental package for scientific computing
import pickle
import math
import time
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
search_win = p[14]
imp_global = p[15]
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
step_imp = 2
pre_pos = 0

#pos = compute_position(imp_global, impC, m, step_imp, laser_pos_imp)
imp = base_imp[4]

size_imp = len(imp_global)
score_min = 1000000
i_min = -1

imp_global = imp_global.astype(np.int16)
imp = imp.astype(np.int16)

start = time.time()

pos = compute_position(imp_global, imp, m, step_imp, laser_pos_imp, pre_pos, search_win)

end = time.time()

print(end - start)

