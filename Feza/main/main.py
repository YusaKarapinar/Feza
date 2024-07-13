from Backgroun_color_func import get_background_color
from Thresholding_background import threshold_background_color
import cv2
import numpy as np
#videoların nuamraları var en güncel video 8. video 8 yazarsanız komut başlayacaktır
#Video_number=str(input("Lütfen Kaçıncı video oldugunu seçiniz:"))
Video_number="8"
cap=cv2.VideoCapture("src/video/vid"+Video_number+".mp4")
ret, frame = cap.read()



print("src/video/vid"+Video_number+".mp4")
while True:
    
    ret, frame = cap.read()
    if ret ==False:
        break

    frame=cv2.resize(frame,(640,480))
    
    background_color=get_background_color(frame)
    print("Arka plan rengi:",background_color)
    threshold=threshold_background_color(frame,background_color)
    final_mask = cv2.erode(threshold, np.ones((3, 3), dtype=np.uint8))
    final_mask = cv2.dilate(final_mask, np.ones((5,5), dtype=np.uint8))
    
    contours, hierarchy = cv2.findContours(final_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    final_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100  and 5000>area:
            final_contours.append(contour)
    final_contours.sort(key=cv2.contourArea, reverse=True)
    debug_img = frame

    cv2.drawContours(debug_img,final_contours,-1, (0, 255, 0), 3)


    
    
    
    
    cv2.imshow('frame', debug_img)
    cv2.imshow('fra', threshold)
    #cv2.imshow('frame', frame)
    #cv2.imshow('threshold', threshold)
    if cv2.waitKey(30) & 0xFF==ord('q'):
        break
    
    
    