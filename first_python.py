import cv2  
import numpy as np  
cap = cv2.VideoCapture("C:\Users\likai\Desktop\WIN_20161025_16_54_51_Pro.mp4")
fgbg1 = cv2.BackgroundSubtractorMOG()  
while(1):  
    ret, frame = cap.read()  
    if ret:  
        fg_mask1 = fgbg1.apply(frame)   
        cv2.imshow('frame', fg_mask1)  
  
        k = cv2.waitKey(30) & 0xff  
        if k == 27:  
           break
    else:  
        break
  
cap.release()  
cv2.destroyAllWindows()  