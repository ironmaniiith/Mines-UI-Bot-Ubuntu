#!/usr/bin/python
import cv2
import numpy as np
from matplotlib import pyplot as plt
from operator import add, sub, div, le, lt

# """
# TODO
def calcAverage(img, x_start, y_start, x_end, y_end, d, w):
    return np.sum(img[x_start:x_end, y_start:y_end])/(d*w)
    # rgb = [0,0,0]
    # for i in xrange(x_start, x_end-20):
    #     for j in xrange(y_start, y_end-20):
    #         print i,j
    #         rgb = map(add, img2[i][j], rgb)
    # print rgb
    # return
    # if flag:
    #     calcAverage(pt, img2)
    #     counter += 1
    #     rgb.append(rgb.pop(0))
    #     print x_start + w/2, y_start + h/2
    #     cv2.rectangle(img2, pt, (x_end, y_end),(rgb[0],rgb[1],rgb[2]), 1)
    #     cv2.putText(img2,str(counter),(x_start+w/3, y_start+h/3), font, 1,(rgb[0], rgb[1], rgb[2]),2)

    # pass    
# """

img = cv2.imread('cropped.png')
img2 = cv2.imread('cropped.png')

# img2 = cv2.imread('fullScreen.jpg')
cv2.imshow('Image', img)
cv2.waitKey(0)

template = cv2.imread('block.png')
d, w, h = template.shape[::-1]
# print d,w,h
res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.98
loc = np.where(res >= threshold)
counter = 0
rgb = [0,255,255]
done = {}
font = cv2.FONT_HERSHEY_SIMPLEX
rgbSum = 0
for pt in zip(*loc[::-1]):
    # Take the sum of all the rgb values from pt[0] -> pt[0] + w and pt[1] -> pt[1]+h in the form of a tuple and then take average.
    # Set a minimum deviation from the actual value and if it's in the deviation is in the range, then take that
    x_start = pt[0]
    x_end = pt[0] + w
    y_start = pt[1]
    y_end = pt[1] + h
    
    num = str(x_start)+str(y_start)
    done[num] = True
    # print (x_start, y_start), img[pt[0]+w/2][pt[1]+h/2]
    flag = True
    for i in xrange(-3, 3):
        for j in xrange(-3, 3):
            if x_start + i >= 0 and y_start + j >= 0 and not(i==0 and j==0):
                num = str(x_start + i) + str(y_start + j)
                try:
                    temp = done[num]
                    flag = False
                    # print "Breaking for " + num
                    break
                except:
                    pass
        if not flag:
            break

    if flag:
        prev = rgbSum
        rgbSum = calcAverage(img2, x_start, y_start, x_end, y_end, d, w)
        counter += 1
        rgb.append(rgb.pop(0))
        print x_start + w/2, y_start + h/2
        cv2.rectangle(img2, pt, (x_end, y_end),(rgb[0],rgb[1],rgb[2]), 1)
        cv2.putText(img2,str(counter) + ":" + str(int(rgbSum)),(x_start+5, y_start+15), font, 0.5,(rgb[0], rgb[1], rgb[2]),2)
cv2.imshow('Response', img2)
cv2.waitKey(0)
cv2.imwrite('res.png',img2)