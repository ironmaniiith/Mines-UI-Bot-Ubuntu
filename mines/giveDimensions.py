#!/usr/bin/python
from __future__ import division
"""
TODO:
	Add comments, explain each argument in the function location_extractor
"""
def calculate_shift(block_size):
	return block_size/1.9

def location_extractor(starting={'x':264, 'y':89}, ending={'x':928, 'y':753}, divisions={'x':8, 'y':8}):
	width, block_size, points =  {}, {}, {}
	keys = ['x', 'y']
	for key in keys:
		width[key] = ending[key] - starting[key]
		block_size[key] = width[key]/divisions[key]
		shift = calculate_shift(block_size[key])
		points[key] = []
		for i in xrange(0,divisions[key]):
			points[key].append(starting[key] + i * block_size[key] + shift)

	locations = []
	for i in points['x']:
		row = []
		for j in points['y']:
			row.append((i,j))
		locations.append(row)
	return locations