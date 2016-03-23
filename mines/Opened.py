#!/usr/bin/python
"""
	returns the array of values corresponding to 0, i.e. the ones which are explored and found to be safe		
"""

from __future__ import division
from modules import *
import GLOBALS

# Status code returned from main
RETURN_STATUS = 0

def is_slightly_deviated(col):
	allowed_deviation = [5,5,5]
	return np.array(map(le, map(abs, map(sub, col, GLOBALS.desired)), allowed_deviation)).all()


def main():
	img = cv2.imread(GLOBALS.cropped_image)
	total_rows = len(img)
	total_cols = len(img[0])

	block_size = (total_rows)/GLOBALS.number_of_blocks
	shift = block_size/2

	count = 0
	rows = []
	for i in xrange(0,GLOBALS.number_of_blocks):
		rows.append((i * block_size) + shift)

	coordinates = []
	for row_count, row in enumerate(rows):
		old = img[row]
		for col_count, col in enumerate(img[row]):
			if (col == old).all():
				count += 1
			else:
				count = 0
			if count >= GLOBALS.consecutive_pixels_count:
				count = 0
				if is_slightly_deviated(col):
					coordinates.append((row_count, int(col_count/block_size)))
			old = col
	# print coordinates, RETURN_STATUS
	return coordinates, RETURN_STATUS