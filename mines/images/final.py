#!/usr/bin/python
from __future__ import division
from operator import add, sub, div, le, lt
import numpy as np
import cv2
import sys, os, re, collections

def is_slightly_deviated(col):
	global desired
	allowed_deviation = [5,5,5]
	return np.array(map(le, map(abs, map(sub, col, desired)), allowed_deviation)).all()

number_of_blocks = 8
desired = [182, 189, 186]
img = cv2.imread('cropped.png')
total_rows = len(img)
total_cols = len(img[0])

block_size = (total_rows)/number_of_blocks
shift = block_size/2

count = 0
rows = []
for i in xrange(0,number_of_blocks):
	rows.append((i * block_size) + shift)

for row_count, row in enumerate(rows):
	old = img[row]
	for col_count, col in enumerate(img[row]):
		if (col == old).all():
			count += 1
		else:
			count = 0
		if count >= 67:
			count = 0
			if is_slightly_deviated(col):
				print row_count, int(col_count/block_size)
		old = col
