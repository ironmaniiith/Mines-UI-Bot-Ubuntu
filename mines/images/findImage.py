#!/usr/bin/python
import cv2
import numpy as np
from matplotlib import pyplot as plt
from operator import add, sub, div, le, lt

def main(image_number):
	image_name = str(image_number) + '.png'
	img = cv2.imread('cropped.png')
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	total_rows = len(img)
	number_of_blocks = 8
	block_size = (total_rows)/number_of_blocks
	shift = block_size/2

	template = cv2.imread(image_name, 0)
	w, h = template.shape[::-1]

	# print d,w,h
	res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.95
	loc = np.where(res >= threshold)
	font = cv2.FONT_HERSHEY_SIMPLEX
	coordinates = []
	for pt in zip(*loc[::-1]):
		# Take the sum of all the rgb values from pt[0] -> pt[0] + w and pt[1] -> pt[1]+h in the form of a tuple and then take average.
		# Set a minimum deviation from the actual value and if it's in the deviation is in the range, then take that
		# print 265+pt[0], 91+pt[1]
		coordinates.append( (int((pt[1]+shift)/block_size), int((pt[0]+shift)/block_size)) )
		# ^^ It is inverted logic, as the dimensions that we get corresponding to x and y are interchanged for rows and columns
	print coordinates
	return coordinates, image_number
