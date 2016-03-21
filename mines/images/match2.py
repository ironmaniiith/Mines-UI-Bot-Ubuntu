import cv2
import numpy as np
# from matplotlib import pyplot as plt

img_rgb = cv2.imread('out.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
template = cv2.imread('temp.png',0)
w, h = template.shape[::-1]

cv2.imshow('rgb', img_rgb)
cv2.waitKey(0)
cv2.imshow('gray', img_gray)
cv2.waitKey(0)
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.4
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
  cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv2.imshow('rgb', img_rgb)
cv2.waitKey(0)
cv2.imwrite('gray.png', img_gray)
cv2.imwrite('res.png',img_rgb)