import cv2
import numpy as np

def threshold_background_color(frame,bgr_color):

    # Tolerans belirleme (renk aralığı)
    tolerance = 30

    # Alt ve üst sınırları belirleme
    lower_bound = np.array([bgr_color[0] - tolerance, bgr_color[1] - tolerance, bgr_color[2] - tolerance])
    upper_bound = np.array([bgr_color[0] + tolerance, bgr_color[1] + tolerance, bgr_color[2] + tolerance])
    mask = cv2.inRange(frame, lower_bound, upper_bound)     

    
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    bgd_mask = cv2.inRange(img_hsv, np.array([0, 0, 0]), np.array([255, 30, 255]))
    
    return ~mask
    #eski kod
    #return ~bgd_mask