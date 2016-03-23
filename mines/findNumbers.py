#!/usr/bin/python
from __future__ import division
from modules import *
import GLOBALS
import findImage

def update_board(board):
	for i in GLOBALS.AVAILABLE_NUMBERS:
		coordinates, image_number = findImage.main(i)
		for j in coordinates:
			board[j[0]][j[1]] = i # i or image_number, whatever :P