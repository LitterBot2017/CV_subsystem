import numpy as np
import cv2

cap = cv2.VideoCapture('C:\Users\likai\Desktop\WIN_20161025_16_54_51_Pro.mp4')

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(4,4))
fgbg = cv2.BackgroundSubtractorMOG()
while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    (cnts,_)=cv2.findContours(fgmask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
    	if cv2.contourArea(c)<50:
    		continue
    	(x,y,w,h)=cv2.boundingRect(c)
    	cv2.rectangle(frame,(x,y),(x+w,y+h),(0, 255, 0), 2)


    
    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()