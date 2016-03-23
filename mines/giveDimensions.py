#!/usr/bin/python
from __future__ import division
"""
TODO:
	Add comments, explain each argument in the function location_extractor
"""
def location_extractor(starting={'x':264, 'y':89}, ending={'x':928, 'y':753}, divisions={'x':8, 'y':8}):
	width =  {}
	width['x'] = ending['x'] - starting['x']
	width['y'] = ending['y'] - starting['y']

	block_size['x'] = width['x']/divisions['x']
	block_size['y'] = width['y']/divisions['y']

	x_points = []
	y_points = []

	for i in xrange(0,divisions['x']):
		x_points.append(starting['x'] + i * block_size['x'] + block_size['x']/1.9)

	for j in xrange(0,divisions['y']):
		y_points.append(starting['y'] + j * block_size['y'] + block_size['y']/1.9)

	locations = []
	for i in x_points:
		row = []
		for j in y_points:
			row.append((i,j))
		locations.append(row)
	return locations