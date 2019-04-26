import cv2
import numpy as np

# FUNCTIONS
def calcul_LS(depth, step, sigma, threshold):
    LS = depth[0:-1:step][0:-1:step]
    condition = np.where(LS > threshold)
    LS[condition] = 0
    LS_blur = cv2.medianBlur(LS, sigma)
    return LS_blur


def compare_LS(LS_base, LS0):
    i_min = 0
    score_min = 1000000
    for i in range(0,len(LS_base)):
        LS = LS_base[i]
        masque = np.abs(LS - LS0)
        score = np.mean(masque)
        if score < score_min:
            score_min = score
            i_min = i
    return [i_min,score_min]


