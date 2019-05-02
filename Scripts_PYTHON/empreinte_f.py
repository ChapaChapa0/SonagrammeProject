import cv2
import numpy as np


# FUNCTIONS
def calcul_empreinte(depth, step, sigma, threshold):
    empreinte = depth[0:-1:step][0:-1:step]
    condition = np.where(empreinte > threshold)
    empreinte[condition] = 0
    empreinte_blur = cv2.medianBlur(empreinte, sigma)
    return empreinte_blur


def calcul_empreinte_global(base_empreinte, m, step):
    n = len(base_empreinte)
    emp_global = base_empreinte[0]
    if n > 1:
        emp0 = emp_global
        for k in range (1,n):
            taille_emp = len(emp0)
            emp = base_empreinte[k]
            score_min = 1000000
            i_min = -1
            emp_fenetre = emp[0:m]
            for i in range (0, taille_emp - m, step):
                emp0_fenetre = emp_global[i : i + m]
                masque = np.abs(emp_fenetre - emp0_fenetre)
                score = np.mean(masque)
                if score < score_min:
                    score_min = score
                    i_min = i
            if i_min == -1:
                raise Exception('error : i_min not found')
            elif i_min + step > taille_emp:
                k1 = taille_emp
            else:
                k1 = i_min + step
            k0 = i_min
            for k in range (k0,k1):
                emp0_fenetre = emp_global[k : k + m]
                masque = np.abs(emp_fenetre - emp0_fenetre)
                score = np.mean(masque)
                if score < score_min:
                    score_min = score
                    k_min = k
            emp0[k_min : -1] = (emp0[k_min : -1] + emp[0 : taille_emp - k_min])/2
            emp0 = np.concatenate((emp0, emp[taille_emp - k_min : -1]), axis = 0)
        emp_global = emp0
    return emp_global


def calcul_position(emp_global, emp, m, step):
    taille_emp = len(emp_global)
    score_min = 1000000
    i_min = -1
    emp_fenetre = emp[0:m]
    for i in range (0, taille_emp - m, step):
        emp_g_fenetre = emp_global[i : i + m]
        masque = np.abs(emp_fenetre - emp_g_fenetre)
        score = np.mean(masque)
        if score < score_min:
            score_min = score
            i_min = i
        if i_min == -1:
            raise Exception('error : i_min not found')
        elif i_min + step > taille_emp:
            k1 = taille_emp
        else:
            k1 = i_min + step
    k0 = i_min
    for k in range (k0,k1):
        emp_g_fenetre = emp_global[k : k + m]
        masque = np.abs(emp_fenetre - emp_g_fenetre)
        score = np.mean(masque)
        if score < score_min:
            score_min = score
            k_min = k
    return k_min
        


