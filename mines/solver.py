#!/usr/bin/python
import os, time, random
import giveDimensions
import findNumbers, findUnOpened, findImage
print "Instructions: "
print "-1: Block not yet revealed."
print "0: Block revealed and is null"
print "1,2,3,4,5: Numbers that are opened"

POSSIBLE_NUMBERS = [-1, 0, 1, 2, 3, 4, 5]
BLOCK_NUMBERS = [num for num in POSSIBLE_NUMBERS if num >0]
board = []
positions = {}
locations = giveDimensions.location_extractor()
TOTAL_MINES_REMAINING = 10
GLOBALS = {
	'mines': -100,
	'safe' : 100,
	'blank' : -1,
}

def inrange(x,board_length):
	return x>=0 and x<board_length

""" ================================ TODO
	Updating the positions dictionary is remaining, just do that
"""

def setProbabilityFlag(x, y):
	""" 
		 _____ _____ _____		 _____ _____ _____ 
		|     |     |     |		|     |     |     |
		| 0,0 | 0,1 | 0,2 |		| 000 | 001 | 010 |
		|_____|_____|_____|		|_____|_____|_____|
		|     |     |     |		|     |     |     |
		| 1,0 | 1,1 | 1,2 |	==>	| 011 |     | 100 |
		|_____|_____|_____|		|_____|_____|_____|
		|     |     |     |		|     |     |     |
		| 2,0 | 2,1 | 2,2 |		| 101 | 110 | 111 |
		|_____|_____|_____|		|_____|_____|_____|
	
		Given, center coordinate, generate all the other remaining coordinates.
		
		s2||s1||s0->  A, B	
		0	0	0 -> -1,-1
		0	0	1 -> -1, 0
		0	1	0 -> -1,+1
		0	1	1 ->  0,-1
		1	0	0 ->  0,+1
		1	0	1 -> +1,-1
		1	1	0 -> +1, 0
		1	1	1 -> +1,+1
		
		Equations:
		A = (!(s1&s0))*(-(!s2)) + (s1|s0)*(s2)
						OR
		Generate A for s2 = 0 and then for s2 = 1, obtain A by putting A = -A (where s1 and s0 bits are same)
		B = (!s2)((s1&!(s0))-(!(s1^s0)))*((s2==1)*-1 + (s2==0))

	# Main code start here
	for s2 in xrange(0,2):
		for s1 in xrange(0,2):
			for s0 in xrange(0,2):
				# print s2,s1,s0
				A = (not(s1&s0))*(-(not(s2))) + (s1|s0)*(s2)
				B = ((s1&(not(s0)))-(not(s1^s0)))
				print A,B
	
	"""


	"""
		Alternate best approach, using just for loops :D
		Yipppeee :D
		But but but, it does not generate the numbers which also satisfy the condition such that 
		x+xdiff>=0 and x+xdiff<=len(board)
					and
		y+ydiff>= 0 and y+ydiff<=len(board)
	"""

	coordinates = [] # Contains all the coordinates of blank boxes
	blank_count = 0
	mines_count = 0
	safe_count = 0
	for xdiff in xrange(-1,2):
		for ydiff in xrange(-1,2,2-xdiff%2):
			x_final = x + xdiff
			y_final = y + ydiff

			if inrange(x_final,8) and inrange(y_final, 8):
				if board[x_final][y_final] == GLOBALS['mines']:
					mines_count += 1
				elif board[x_final][y_final] == GLOBALS['safe']:
					safe_count += 1
				elif board[x_final][y_final] == GLOBALS['blank']:
					coordinates.append((x+xdiff, y+ydiff))
					blank_count += 1
				# print (x+xdiff,y+ydiff)

	return coordinates, { 'blank_count': blank_count, 'safe_count': safe_count, 'mines_count': mines_count }
	"""
		The whole target of the above code was to go to the generate all the neighbouring places of a given center coordinate
		((1,1) in this case)
	"""

class Solver():
	"""
		Solver class for the board
	"""
	def __init__(self):
		pass
	def mark_all(self, board, blocks_coordinates, flag):
		global TOTAL_MINES_REMAINING
		status = False
		for coordinate in blocks_coordinates:
			if board[coordinate[0]][coordinate[1]] != flag:
				print "Marking flag = {0} at {1}".format(flag, (coordinate[0], coordinate[1]))
				board[coordinate[0]][coordinate[1]] = flag
				TOTAL_MINES_REMAINING -= (flag == GLOBALS['mines'])
				print "TOTAL_MINES_REMAINING = " + str(TOTAL_MINES_REMAINING)
				status = True
		return status
	def mark_safe(self):
		pass
	def mark_mines(self):
		pass
	def assign_probability(self):
		pass

def is_game_finished():
	print 'is_game_finished================================='
	coordinates, x = findImage.main('finished')
	if len(coordinates):
		exit(0)
	return False

def getInputOfBlocks():
	print 'Taking new input'
	global board
	board = []
	global positions
	positions = {}

	for i in POSSIBLE_NUMBERS:
		positions[str(i)] = []

	# os.system('xdotool mousemove 9 100') # Just remove the mouse before taking screenshot
	os.system('xwininfo -root -tree  | grep -i -e "gnome-mine" -e "Print Cart"| egrep -o "[0-9a-fA-F]+x[0-9a-fA-F]+" | head -1 > id')
	os.system('xdotool windowactivate `cat id`')
	time.sleep(0.1)
	os.system('scrot -q 100 fullScreen.png')
	os.system('convert -crop 670x670+260+85 fullScreen.png cropped.png')
	for i in xrange(0,8):
		board.append([-1]*8)

	if is_game_finished():
		exit(0)
	findNumbers.update_board(board)
	findUnOpened.update_board(board)
	for i in xrange(0,8):
		for j in xrange(0,8):
			positions[str(board[i][j])].append((i,j))
	print board

def click(i,j,click_type=1):
	time.sleep(0.15)
	os.system("xdotool mousemove {0} {1} click {2}".format(locations[i][j][0], locations[i][j][1], click_type))
	print "clicking {0} {1}".format(locations[i][j][0], locations[i][j][1])
	return

def clickRandom(board_length=8):
	i,j = random.choice(positions['-1'])
	click(j,i)
	return
	for i in xrange(0,board_length):
		for j in xrange(0,board_length):
			if board[i][j] == -1:
				click(j,i)
				return

def clickOnSafeFlags(board_length):
	print "Going to start clickOnSafeFlags"
	was_clicked = False
	for i in xrange(0,board_length):
		for j in xrange(0, board_length):
			if board[i][j] == GLOBALS['safe']:
				click(j,i)
				was_clicked = True
	return was_clicked
counter = 0

while TOTAL_MINES_REMAINING != 0:
	getInputOfBlocks()
	TOTAL_MINES_REMAINING = 10
	solver = Solver()
	while True:
		print "==========================================================="
		flag = False
		for val in BLOCK_NUMBERS:
			print "Iterating for val = {0}".format(val)
			position = positions[str(val)]
			for coordinates in position:
				blocks_coordinates, counts = setProbabilityFlag(coordinates[0], coordinates[1])
				s = "{0}, {1} ->".format((coordinates[0], coordinates[1]),val)
				print s,
				print blocks_coordinates, counts
				if counts['mines_count'] == val and counts['blank_count'] > 0:
					print "marking safe the coordinates: {0}".format(blocks_coordinates)
					status = solver.mark_all(board, blocks_coordinates, GLOBALS['safe'])
					if status:
						flag = True
				elif counts['blank_count'] <= val-counts['mines_count']:
					# All the mines
					status = solver.mark_all(board, blocks_coordinates, GLOBALS['mines'])
					if status:
						flag = True
			print board
		if flag == False:
			print "Breaking, more information needed for proceeding"
			was_clicked = clickOnSafeFlags(8)
			if not was_clicked:
				print "Not clicked"
				counter += 1
			if counter == 2:
				counter = 0
				print 'Board before calling the random is {0}'.format(board)
				print 'Click random'
				clickRandom()
			break
print 'Game ended, all flags found'

if not is_game_finished():
	# If the message box that says that the game is finished has not yet come, then mark all the mines
	for i in xrange(0,8):
		for j in xrange(0,8):
			if board[i][j] == -100:
				click(j,i,3)