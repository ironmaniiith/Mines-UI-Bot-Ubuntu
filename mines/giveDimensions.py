#!/usr/bin/python
from __future__ import division
# starting_x = int(raw_input(""))
# starting_y = int(raw_input(""))
# ending_x = int(raw_input(""))
# ending_y = int(raw_input(""))
# 
# divisions_x = int(raw_input(""))
# divisions_y = int(raw_input(""))

def location_extractor():
	starting_x = 264
	starting_y = 89
	ending_x = 928
	ending_y = 753
	divisions_x = 8
	divisions_y = 8

	width_x = ending_x - starting_x
	width_y = ending_y - starting_y
	# print width_x, divisions_x
	block_size_x = width_x/divisions_x
	block_size_y = width_y/divisions_y
	# print block_size_x, block_size_y
	x_points = []
	y_points = []

	for i in xrange(0,divisions_x):
		x_points.append(starting_x + i * block_size_x + block_size_x/1.9)

	for j in xrange(0,divisions_y):
		y_points.append(starting_y + j * block_size_y + block_size_y/1.9)
	# print x_points	
	# print y_points
	locations = []
	for i in x_points:
		row = []
		for j in y_points:
			row.append((i,j))
		locations.append(row)
	return locations