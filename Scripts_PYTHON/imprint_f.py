import cv2
import numpy as np


# FUNCTIONS
def compute_imprint(depth, win_h, win_w, step, sigma, threshold):
    depth0 = np.transpose(depth[win_h[0]: win_h[1]])
    depth0 = np.transpose(depth0[win_w[0]:win_w[1]])
    imprint = depth0
    condition = np.where(imprint > threshold)
    if condition:
        imprint[condition] = 0
    imprint_blur = cv2.medianBlur(imprint, sigma)
    return imprint_blur


def compute_imprint_global(base_imprint, m, step):
    n = len(base_imprint)
    step0 = step[0]
    step1 = step[1]
    if n > 1:
        imp0 = base_imprint[0]
        for k in range (1,n):
            size_imp = len(imp0)
            imp = base_imprint[k]
            score_min = 1000000
            i_min = -1
            imp_win = imp[0 : 2*m]
            for i in range (m, size_imp - m, step0):
                imp0_win = imp0[i - m : i + m]
                mask1 = np.abs(imp_win - imp0_win)
                mask2 = np.abs(imp0_win - imp_win)
                score = np.mean(mask1) + np.mean(mask2)
                if score < score_min:
                    score_min = score
                    i_min = i
            if i_min == -1:
                raise Exception('error : i_min not found')
            k0 = i_min
            k1 = i_min + step0
            k_min = i_min
            for k in range (k0, k1, step1):
                imp0_win = imp0[k - m : k + m]
                mask1 = np.abs(imp_win - imp0_win)
                mask2 = np.abs(imp0_win - imp_win)
                score = np.mean(mask1) + np.mean(mask2)
                if score < score_min:
                    score_min = score
                    k_min = k
            p = size_imp - (k_min + m)
            print(p)
            print(k_min)
            if p < len(imp) - 2*m:
                imp0 = np.concatenate((imp0, imp[p + 2*m : -1]), axis = 0)
        imp_global = imp0
    else:
        imp_global = base_imprint[0]
    return imp_global


def compute_position(imp_global, imp, m, step, laser_pos):
    size_imp = len(imp_global)
    score_min = 1000000
    i_min = -1
    imp_win = imp[laser_pos - m : laser_pos + m]
    step0 = step[0]
    step1 = step[1]
    
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
    position = k_min
    return position
        


