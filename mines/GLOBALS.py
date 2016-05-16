#!/usr/bin/python
from modules import *
import giveDimensions

"""
	number_of_blocks : The blocks present in the current board configuration (should be detected automatically later on)
"""
number_of_blocks = 8

"""
	threshold : Threshold while matching images
"""
threshold = 0.92

"""
	cropped_image : The image containing the cropped image of the board
"""
cropped_image = 'cropped.png'

"""
	font : cv2 font that can be used for debugging
"""
font = cv2.FONT_HERSHEY_SIMPLEX

"""
	TOTAL_MINES_REMAINING : Self explainatory
"""
TOTAL_MINES_REMAINING = 10

"""
	desired: Desired rgb values of the required block (Here it is the block which is explored and opened)
"""
desired = [220, 222, 222]
# desired = [182, 189, 186]

"""
	allowed_deviation : Deviation allowed during matching of any image 
"""
allowed_deviation = [5,5,5]

"""
	consecutive_pixels_count : The number of consecutive pixels with same rgb values (used to detect block in the board)
"""
consecutive_pixels_count = 67

"""
	AVAILABLE_NUMBERS : Numbers currently available (i.e. which can be detected on the board)
"""
AVAILABLE_NUMBERS = [1, 2, 3, 4, 5]

"""
	POSSIBLE_NUMBERS : The set of numbers used for assigning values in the board list (used in solver.py)
"""
POSSIBLE_NUMBERS = [-1, 0, 1, 2, 3, 4, 5]

"""
	BLOCK_NUMBERS : Positive numbers among POSSIBLE_NUMBERS
"""
BLOCK_NUMBERS = [num for num in POSSIBLE_NUMBERS if num > 0]

"""
	Block codes used in the game logic to represent the board with their respective values.
"""
BLOCK_CODES = {
	'mines' : -100,
	'safe' : 100,
	'blank' : -1,
}

"""
	Below are the helping values required for finding the coordinates in pixels using location function in giveDimensions
	starting : Dictionary containing the x and y coordinates of board's actual starting pixel
	ending : Dictionary containing the x and y coordinates of board's actual ending pixel
	divisions : Dictionary containing the x and y divisions in the current board, ideally should be equal to number_of_blocks
"""
starting, ending, divisions = {}, {}, {}
starting['x'] = 264
starting['y'] = 89
ending['x'] = 927
ending['y'] = 752
divisions['x'] = 8
divisions['y'] = 8
# starting['x']-starting['y'] == ending['x'] - ending['y'] for a square board

"""
	locations : List containing the pixel value of the coordinate.
	How to use : Suppose if you want to find the pixel value (or location) when coordinate is given (say (3,4)).
	Now for (3,4), locations[3][4] gives the coordinate (in terms of pixels) which can be used for clicking or similar purposes.
"""
locations = giveDimensions.location_extractor(starting, ending, divisions)
