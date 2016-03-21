#!/usr/bin/python
from __future__ import division
from operator import add, sub, div, le, lt
import numpy as np
import cv2
import sys, os, re, collections
import findImage
AVAILABLE_NUMBERS = [1, 2, 3, 4]

def update_board(board):
	for i in AVAILABLE_NUMBERS:
		coordinates, image_number = findImage.main(i)
		for j in coordinates:
			board[j[0]][j[1]] = i # i or image_number, whatever :P