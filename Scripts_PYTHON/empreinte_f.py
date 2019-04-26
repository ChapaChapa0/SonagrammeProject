import cv2
import numpy as np

# FUNCTIONS
def calcul_empreinte(depth, step, sigma, threshold):
    empreinte = depth[0:-1:step][0:-1:step]
    condition = np.where(empreinte > threshold)
    empreinte[condition] = 0
    empreinte_blur = cv2.medianBlur(empreinte, sigma)
    return empreinte_blur


def calcul_empreinte_global(base_empreinte, step, sigma, threshold):
    empreinte_global = []
    for i in range (0,len(base_empreinte)):
        0

    return empreinte_global


def calcul_position(empreinte_global, empreinte):

    return 0


