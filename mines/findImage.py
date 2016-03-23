#!/usr/bin/python
import GLOBALS
import cv2, numpy as np
"""
TODO:
	Rename function from main to something else
	Add comments
"""

def main(image_name):
	template_image = str(image_name) + '.png'
	img = cv2.imread(GLOBALS.cropped_image)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	total_rows = len(img)
	block_size = (total_rows)/GLOBALS.number_of_blocks
	shift = block_size/2

	template = cv2.imread(template_image, 0)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
	loc = np.where(res >= GLOBALS.threshold)
	coordinates = []
	for pt in zip(*loc[::-1]):
		coordinates.append( (int((pt[1]+shift)/block_size), int((pt[0]+shift)/block_size)) )
		# ^^ It is inverted logic, as the dimensions that we get corresponding to x and y are interchanged for rows and columns
	# print coordinates
	return coordinates, image_name
