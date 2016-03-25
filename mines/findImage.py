#!/usr/bin/python
from modules import *
import GLOBALS
"""
TODO:
	Rename function from main to something else
	Add comments
"""

def main(image_name, image=GLOBALS.cropped_image, block_size=None, shift=None):
	template_image = str(image_name) + '.png'
	image = cv2.imread(image)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to gray

	total_rows = len(image)
	block_size = block_size or (total_rows)/GLOBALS.number_of_blocks
	shift = shift or block_size/2

	template = cv2.imread(template_image, 0)
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
	loc = np.where(res >= GLOBALS.threshold)
	coordinates = []
	for pt in zip(*loc[::-1]):
		coordinates.append((int((pt[1]+shift)/block_size), int((pt[0]+shift)/block_size)))
		# ^^ It is inverted logic, as the dimensions that we get corresponding to x and y are interchanged for rows and columns
	# print coordinates
	return coordinates, image_name
