import cv2
import numpy as np


# FUNCTIONS
def compute_imprint(depth, win_h, win_w, step, sigma, threshold):
    depth0 = np.transpose(depth[win_h[0] : win_h[1]])
    depth1 = depth0[win_w[0] : win_w[1]]
    imprint = depth1
    condition = np.where(imprint > threshold)
    if condition:
        imprint[condition] = 0
    imprint_blur = cv2.medianBlur(imprint, sigma)
    return imprint_blur


def compute_imprint_global(base_imprint, m, step, laser_pos):
    n = len(base_imprint)
    if n > 1:
        imp0 = base_imprint[0].astype(np.int16)
        for k in range (1,n):
            size_imp = len(imp0)
            imp = base_imprint[k].astype(np.int16)
            score_min = 1000000
            i_min = -1
            imp_win = imp[0 : 2*m]
            for i in range (m, size_imp - m, step):
                imp0_win = imp0[i - m : i + m]
                mask = np.abs(imp_win - imp0_win)
                score = np.mean(mask)
                if score < score_min:
                    score_min = score
                    i_min = i
            if i_min == -1:
                raise Exception('error : i_min not found')
            p = size_imp - (i_min + m)
            if p < len(imp) - 2*m:
                imp0 = np.concatenate((imp0, imp[p + 2*m : -1]), axis = 0)
        imp_global = imp0.astype(np.uint16)
    else:
        imp_global = base_imprint[0]
    return imp_global


def compute_imprint_global_nul(base_imprint, m, step, laser_pos):
    n = len(base_imprint)
    imp0 = base_imprint[0]
    imp0 = imp0[laser_pos : -1]
    for i in range (1,n):
        imp = base_imprint[i]
        imp = imp[laser_pos : -1]
        imp0 = np.concatenate((imp0, imp), axis = 0)
    imp_global = imp0
    return imp_global


def compute_position(imprint_global, imprint, m, step, laser_pos, pre_pos, search_win):
    size_imp = len(imprint_global)
    score_min = 1000000
    k_min = -1

    imp_global = imprint_global.astype(np.int16)
    imp = imprint.astype(np.int16)
    imp_win = imp[laser_pos : laser_pos + m]

    if pre_pos + search_win > size_imp - m:
        k1 = size_imp - m
    else:
        k1 = pre_pos + search_win
    if pre_pos - search_win < 0:
        k0 = 0
    else:
        k0 = pre_pos - search_win
    for k in range (k0, k1, step):
        imp_g_win = imp_global[k : k + m]
        mask1 = np.abs(imp_g_win - imp_win)
        score = np.mean(mask1)
        if score < score_min:
            score_min = score
            k_min = k
    if k_min == -1:
        raise Exception('error : k_min not found')
    position = k_min
    return position
                
        

