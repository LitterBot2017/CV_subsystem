import numpy as np
import cv2
import math


def nothing(*arg):
    pass

def make_odd(val):
    if val % 2 == 0:
        val += 1

    return val

def findSignificantContours (img, edge_image):
    # image, 

    contours, heirarchy = cv2.findContours(edge_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if heirarchy is None:
        return None

    # Find level 1 contours
    level1 = []
    for i, tupl in enumerate(heirarchy[0]):
        # Each array is in format (Next, Prev, First child, Parent)
        # Filter the ones without parent
        if tupl[3] == -1:
            tupl = np.insert(tupl, 0, [i])
            level1.append(tupl)
    # From among them, find the contours with large surface area.
    significant = []
    # tooSmall = edge_image.size * 0.00005 # If contour isn't covering 5% of total area of image then it probably is too small
    # tooSmall = edge_image.size * 1 / 100 # If contour isn't covering 5% of total area of image then it probably is too small
    tooSmall = 0.0005 * edge_image.size
    tooBig = 0.001*edge_image.size
    # tooSmall = 0.0
    for tupl in level1:
        contour = contours[tupl[0]];
        (x,y),radius = cv2.minEnclosingCircle(contour)
        area = math.pi*radius*radius
        # area = cv2.contourArea(contour)
        if area > tooSmall and area< tooBig :
            significant.append([contour, area])

            # Draw the contour on the original image
            cv2.drawContours(img, [contour], 0, (0,255,0),2, cv2.cv.CV_AA, maxLevel=1)
            cv2.circle(img,(int(x),int(y)),int(radius),(0,255,0),2)

    significant.sort(key=lambda x: x[1])
    #print ([x[1] for x in significant]);
    return [x[0] for x in significant];

cap = cv2.VideoCapture('WIN_20161025_16_54_51_Pro.mp4')

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(4,4))
fgbg = cv2.BackgroundSubtractorMOG()

window_nm = 'img_cntrls'
cv2.namedWindow(window_nm)
cv2.createTrackbar('blur_size', window_nm, 15 , 21, nothing)
cv2.createTrackbar('thresh_min', window_nm, 200 , 255, nothing)


while(1):
    thresh_min  = cv2.getTrackbarPos('thresh_min',window_nm)

    blur_size = cv2.getTrackbarPos('blur_size',window_nm)
    blur_size = make_odd(blur_size)

    ret, frame = cap.read()
    if (ret == True):
	    fgmask = fgbg.apply(frame)
	    

	    fgmask = cv2.blur(fgmask, (blur_size, blur_size))
	    # fgmask = cv2.GaussianBlur(fgmask, (blur_size, blur_size), 0) # Remove noise

	    # cv2.threshold(blur, thresh_min, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	    # fgmask = cv2.adaptiveThreshold(fgmask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blur_size, 0)
	    # fgmask = cv2.adaptiveThreshold(fgmask, 255, cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY, blur_size, 0)
	    ret, fgmask = cv2.threshold(fgmask, thresh_min, 255, cv2.THRESH_BINARY)

	    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

	    findSignificantContours (frame, fgmask)

	    # cv2.imshow('frame',fgmask)
	    cv2.imshow('frame',frame)
    else:
        video_capture.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO,0)
        cv2.destroyAllWindows()
        exit()

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()