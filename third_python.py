import numpy as np
import cv2
import math


def nothing(*arg):
    pass

def make_odd(val):
    if val % 2 == 0:
        val += 1

    return val

def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in xrange(row1):
        for j in xrange(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 50 :
                return True
            elif i==row1-1 and j==row2-1:
                return False

cap = cv2.VideoCapture('C:\Users\likai\Desktop\Study\MRSD Project\CV_subsystem\WIN_20161025_16_54_51_Pro.mp4')

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 4))
fgbg = cv2.BackgroundSubtractorMOG()

while (1):
    ret, frame = cap.read()
    blur_size=20
    fgmask = fgbg.apply(frame)
    fgmask = cv2.blur(fgmask, (blur_size, blur_size))
    ret, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    contours, heirarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find level 1 contours
    level1 = []
    if heirarchy is not None:
        for i, tupl in enumerate(heirarchy[0]):
            # Each array is in format (Next, Prev, First child, Parent)
            # Filter the ones without parent
            if tupl[3] == -1:
                tupl = np.insert(tupl, 0, [i])
                level1.append(tupl)
        # From among them, find the contours with large surface area.
        significant = []
        tooSmall = 0.0005 * fgmask.size
        tooBig = 0.001*fgmask.size
        LENGTH = len(contours)
        status = np.zeros((LENGTH, 1))

        for tupl in level1:
            contour = contours[tupl[0]]
            x, y, w, h = cv2.boundingRect(contour)
            area=w*h
            #  (x,y),radius = cv2.minEnclosingCircle(contour)
           # area = math.pi*radius*radius
            if area > tooSmall:
                # significant.append([contour, area])

                for i, cnt1 in enumerate(contours):
                    x = i
                    if i != LENGTH - 1:
                        for j, cnt2 in enumerate(contours[i + 1:]):
                            x = x + 1
                            dist = find_if_close(cnt1, cnt2)
                            if dist == True:
                                val = min(status[i], status[x])
                                status[x] = status[i] = val
                            else:
                                if status[x] == status[i]:
                                    status[x] = i + 1

                unified = []
                maximum = int(status.max()) + 1
                for i in xrange(maximum):
                    pos = np.where(status == i)[0]
                    if pos.size != 0:
                        cont = np.vstack(contours[i] for i in pos)
                        hull = cv2.convexHull(cont)
                        unified.append(hull)
                for tupl in level1:
                    contour1 = contours[tupl[0]]
                    x1, y1, w1, h1 = cv2.boundingRect(contour1)
                    area1=w1*h1
                    if area1<tooBig:
                        cv2.drawContours(frame, unified, -1, (0, 255, 0), 2)
                        cv2.drawContours(fgmask, unified, -1, 255, -1)
                        cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                        print(x1,y1)

                #cv2.drawContours(frame, [contour], 0, (0,255,0),2, cv2.cv.CV_AA, maxLevel=1)
                 #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)



    cv2.imshow('frame', fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()