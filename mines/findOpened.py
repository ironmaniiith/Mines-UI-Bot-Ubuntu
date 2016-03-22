#!/usr/bin/python
import Opened
def update_board(board):
	coordinates, image_number = Opened.main()
	for j in coordinates:
		board[j[0]][j[1]] = image_number