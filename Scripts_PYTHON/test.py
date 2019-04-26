import cv2
from matplotlib import pyplot as plt

depth = depth_init

cv2.imshow('image', depth)
cv2.waitKey(0)
cv2.destroyAllWindows()