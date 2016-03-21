#!/usr/bin/python
import numpy as np
import cv2
import getopt, sys

def findCenter(x):
	return (sum(x))/len(x)

def PolygonArea(corners):
	n = len(corners) # of corners
	area = 0.0
	for i in range(n):
		j = (i + 1) % n
		area += corners[i][0] * corners[j][1]
		area -= corners[j][0] * corners[i][1]
	area = abs(area) / 2.0
	return area
CANNY=[10,10]

def getopts():
	d={}
	d['xOffset'] = 0
	d['yOffset'] = 0
	d['color'] = "RGB2GRAY"
	d['area'] = 5000000
	try:
		opts, args = getopt.getopt(sys.argv[1:], "x:y:c:a:o:i:cn:", ["xOffset=", "yOffset=", "color=", "area=", "output=", "input=", "canny="])
		for opt, arg in opts:
			if opt in ("-x","--xOffset"):
				xOffset = int(arg)
			if opt in ("-y","--yOffset"):
				yOffset = int(arg)
			if opt in ("-c","--color"):
				color = arg
			if opt in ("-o", "--output"):
				global OUTPUT_FILE
				OUTPUT_FILE = arg
			if opt in ("-i", "--input"):
				global INPUT_FILE
				INPUT_FILE = arg
			if opt in ("-a","--area"):
				area = int(arg)
			if opt in ("-cn","--canny"):
				global CANNY 
				CANNY = map(int, arg.split(":"))								
		d['xOffset'] = xOffset
		d['yOffset'] = yOffset
		d['color'] = color
		d['area'] = area
		return d
	except Exception, e:
		print "Some exception"
		pass
	return d

d = getopts()
print d
xOffset = d['xOffset']
yOffset = d['yOffset']
color = d['color']
area = d['area']
print CANNY
print INPUT_FILE

image = cv2.imread(INPUT_FILE)
gray = cv2.cvtColor(image, eval("cv2.COLOR_" + color))
gray = cv2.GaussianBlur(gray, (3,3), 0)

cv2.imshow('Gray', gray)
cv2.waitKey(0)

edged = cv2.Canny(gray, CANNY[0], CANNY[1]) # Set both these values to very low and handle this case later
# Later on the points are taken into consideration based on the area of the polygon that we obtain

cv2.imshow('Edged', edged)
cv2.waitKey(0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

cv2.imshow('Closed', closed)
cv2.waitKey(0)

(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
total = 0
open('coordinates.temp', 'w').close()
for c in cnts:
	peri = cv2.arcLength(c,True)
	approx = cv2.approxPolyDP(c, 0.1 * peri, True)
	if len(approx) == 4 or len(approx) == 3:
		cv2.drawContours(gray, [approx], -1, (0,255,0), len(approx))
		total+=1
		x = []
		y = []
		points = []
		for i in approx:
			x.append(i[0][0])
			y.append(i[0][1])
			points.append((i[0][0],i[0][1]))
		dec = PolygonArea(points)
		print dec
		if dec >= area:
			print x,y
			xCenter = findCenter(x)
			yCenter = findCenter(y)
			with open('coordinates.temp', 'a') as f:
				f.write(str(xCenter+xOffset)+":"+str(yCenter+yOffset) + "\n") 

if total == 0:
	exit(1)
# print "Found total of {0} rect in the image ".format(total)

cv2.imshow("Final Output", gray)
cv2.waitKey(0)
print OUTPUT_FILE
cv2.imwrite(OUTPUT_FILE, gray)
exit(0)