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
    imp_global = base_imprint[0]
    if n > 1:
        imp0 = imp_global
        for k in range (1,n):
            size_imp = len(imp0)
            imp = base_imprint[k]
            score_min = 1000000
            i_min = -1
            imp_fenetre = imp[0:m]
            for i in range (0, size_imp - m, step[0]):
                imp0_fenetre = imp_global[i : i + m]
                masque = np.abs(imp_fenetre - imp0_fenetre)
                score = np.mean(masque)
                if score < score_min:
                    score_min = score
                    i_min = i
            if i_min == -1:
                raise Exception('error : i_min not found')
            elif i_min + step > size_imp:
                k1 = size_imp
            else:
                k1 = i_min + step
            k0 = i_min
            for k in range (k0,k1,step[1]):
                imp0_fenetre = imp_global[k : k + m]
                masque = np.abs(imp_fenetre - imp0_fenetre)
                score = np.mean(masque)
                if score < score_min:
                    score_min = score
                    k_min = k
            imp0[k_min : -1] = (imp0[k_min : -1] + imp[0 : size_imp - k_min])/2
            imp0 = np.concatenate((imp0, imp[size_imp - k_min : -1]), axis = 0)
        imp_global = imp0
    return imp_global


def compute_position(imp_global, imp, m, step):
    size_imp = len(imp_global)
    score_min = 1000000
    i_min = -1
    imp_fenetre = imp[0:m]
    for i in range (0, size_imp - m, step[0]):
        imp_g_fenetre = imp_global[i : i + m]
        masque = np.abs(imp_fenetre - imp_g_fenetre)
        score = np.mean(masque)
        if score < score_min:
            score_min = score
            i_min = i
        if i_min == -1:
            raise Exception('error : i_min not found')
        elif i_min + step > size_imp:
            k1 = size_imp
        else:
            k1 = i_min + step
    k0 = i_min
    for k in range (k0,k1,step[1]):
        imp_g_fenetre = imp_global[k : k + m]
        masque = np.abs(imp_fenetre - imp_g_fenetre)
        score = np.mean(masque)
        if score < score_min:
            score_min = score
            k_min = k
    return k_min
        


