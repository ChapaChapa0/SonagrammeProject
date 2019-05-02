import cv2
import numpy as np


# FUNCTIONS
def compute_imprint(depth, step, sigma, threshold):
    imprint = depth[0:-1][0:-1]
    condition = np.where(imprint > threshold)
    imprint[condition] = 0
    imprint_blur = cv2.medianBlur(imprint, sigma)
    return imprint_blur


def compute_imprint_global(base_imprint, m, step):
    n = len(base_imprint)
    imp0 = base_imprint[0]
    step0 = step[0]
    step1 = step[1]
    if n > 1:
        for k in range (1,n):
            size_imp = len(imp0)
            imp = base_imprint[k]
            score_min = 1000000
            i_min = -1
            imp_window = imp[0:m]
            for i in range (0, size_imp - m, step0):
                imp0_window = imp0[i : i + m]
                mask1 = np.abs(imp_window - imp0_window)
                mask2 = np.abs(imp0_window - imp_window)
                score = np.mean(mask1) + np.mean(mask2)
                if score < score_min:
                    score_min = score
                    i_min = i
            if i_min == -1:
                raise Exception('error : i_min not found')
            elif i_min + step0 > size_imp:
                k1 = size_imp
            else:
                k1 = i_min + step0
            k0 = i_min
            k_min = i_min
            for k in range (k0, k1, step1):
                imp0_window = imp0[k : k + m]
                masque = np.abs(imp_window - imp0_window)
                score = np.mean(masque)
                if score < score_min:
                    score_min = score
                    k_min = k
            imp0[k_min : -1] = (imp0[k_min : -1] + imp[0 : size_imp - k_min - 1])/2
            imp0 = np.concatenate((imp0, imp[size_imp - k_min - 1 : -1]), axis = 0)
    imp_global = imp0
    return imp_global


def compute_position(imp_global, imp, m, step):
    size_imp = len(imp_global)
    score_min = 1000000
    i_min = -1
    imp_window = imp[0:m]
    step0 = step[0]
    step1 = step[1]
    for i in range (0, size_imp - m, step0):
        imp_g_window = imp_global[i : i + m]
        masque = np.abs(imp_window - imp_g_window)
        score = np.mean(masque)
        if score < score_min:
            score_min = score
            i_min = i
        if i_min == -1:
            raise Exception('error : i_min not found')
        elif i_min + step0 > size_imp:
            k1 = size_imp
        else:
            k1 = i_min + step0
    k0 = i_min
    for k in range (k0,k1,step1):
        imp_g_window = imp_global[k : k + m]
        masque = np.abs(imp_window - imp_g_window)
        score = np.mean(masque)
        if score < score_min:
            score_min = score
            k_min = k
    return k_min
        


