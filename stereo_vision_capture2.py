import numpy as np
import cv2


#video_writer_right = cv2.VideoWriter(file_name+'_right.avi', cv2.cv.CV_FOURCC('M','J','P','G'), 29, (1280,720), 1)
# video_writer_left = cv2.VideoWriter(file_name+'_left.avi', cv2.cv.CV_FOURCC('M','J','P','G'), 29, (1280,720), 1)

video_capture_left = cv2.VideoCapture(1)
video_capture_right = cv2.VideoCapture(0)

#fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
out = cv2.VideoWriter('output.avi',-1,20.0,(640,480))
out2 = cv2.VideoWriter('output2.avi',-1,20.0,(640,480))

while True:
    ret, img_left = video_capture_left.read()
    ret, img_right = video_capture_right.read()
    if (ret == True):

        img_left = cv2.flip(img_left,0)
        img_right =cv2.flip(img_right,0)
        out.write(img_left)
        out2.write(img_right)
        cv2.imshow('img_left', img_left)
        cv2.imshow('img_right',img_right)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break



# When everything is done, release the capture
video_capture_left.release()
video_capture_right.release()

out.release()
out2.release()
cv2.destroyAllWindows()