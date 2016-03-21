#!/usr/bin/python
import unOpened
def update_board(board):
	coordinates, image_number = unOpened.main()
	for j in coordinates:
		board[j[0]][j[1]] = image_number