#!/usr/bin/python
from modules import *
import GLOBALS
import giveDimensions
import findNumbers, findOpened, findImage

print "Instructions: "
print "-1: Block not yet revealed."
print "0: Block revealed and is null"
print "1,2,3,4,5: Numbers that are opened"

# POSSIBLE_NUMBERS = [-1, 0, 1, 2, 3, 4, 5]
# BLOCK_NUMBERS = [num for num in POSSIBLE_NUMBERS if num >0]
board = []
positions = {}
mines_remaining = GLOBALS.TOTAL_MINES_REMAINING
# locations = giveDimensions.location_extractor()
# TOTAL_MINES_REMAINING = 10
# GLOBALS = {
	# 'mines': -100,
	# 'safe' : 100,
	# 'blank' : -1,
# }

def inrange(x,board_length=GLOBALS.number_of_blocks):
	return x >= 0 and x < board_length

""" ================================ TODO
	Updating the positions dictionary is remaining, just do that
	Rename this setProbabilityFlag function
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
				if board[x_final][y_final] == GLOBALS.BLOCK_CODES['mines']:
					mines_count += 1
				elif board[x_final][y_final] == GLOBALS.BLOCK_CODES['safe']:
					safe_count += 1
				elif board[x_final][y_final] == GLOBALS.BLOCK_CODES['blank']:
					coordinates.append((x+xdiff, y+ydiff))
					blank_count += 1

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
		status = False
		global mines_remaining
		for coordinate in blocks_coordinates:
			if board[coordinate[0]][coordinate[1]] != flag:
				board[coordinate[0]][coordinate[1]] = flag
				mines_remaining -= (flag == GLOBALS.BLOCK_CODES['mines'])
				status = True
		return status
	"""
		Remove the below functions if not necessary
	"""
	def mark_safe(self):
		pass
	def mark_mines(self):
		pass
	def assign_probability(self):
		pass

def is_game_finished():
	coordinates, x = findImage.main('finished') # finished.png is the image when the game is finished
	if len(coordinates):
		exit(0)
	return False

def getInputOfBlocks():
	global board
	board = []
	global positions
	positions = {}

	for i in GLOBALS.POSSIBLE_NUMBERS:
		positions[str(i)] = []

	# Avoid writing into the file 'id' and use subprocess later
	os.system('xwininfo -root -tree  | grep -i -e "gnome-mine" -e "Print Cart"| egrep -o "[0-9a-fA-F]+x[0-9a-fA-F]+" | head -1 > id')
	os.system('xdotool windowactivate `cat id`')
	time.sleep(0.1)
	os.system('scrot -z -q 100 fullScreen.png') # Search for alternative screenshot method which is preinstalled in most systems
	os.system('convert -crop 670x670+260+85 fullScreen.png cropped.png')
	for i in xrange(0,GLOBALS.number_of_blocks):
		board.append([-1]*GLOBALS.number_of_blocks)

	if is_game_finished():
		exit(0)
	findNumbers.update_board(board)
	findOpened.update_board(board)
	for i in xrange(0,GLOBALS.number_of_blocks):
		for j in xrange(0,GLOBALS.number_of_blocks):
			positions[str(board[i][j])].append((i,j))
	# print board

def click(i,j,click_type=1):
	time.sleep(0.1)
	os.system("xdotool mousemove {0} {1} click {2}".format(GLOBALS.locations[i][j][0], GLOBALS.locations[i][j][1], click_type))
	# print "clicking {0} {1}".format(locations[i][j][0], locations[i][j][1])
	return

def clickRandom(board_length=GLOBALS.number_of_blocks):
	shuf = []
	for i in xrange(0, board_length):
		for j in xrange(0, board_length):
			if board[i][j] == GLOBALS.BLOCK_CODES['blank']:
				shuf.append((i,j))
	i,j = random.choice(shuf)
	click(j,i)

def clickOnSafeFlags(board_length=GLOBALS.number_of_blocks):
	was_clicked = False
	for i in xrange(0, board_length):
		for j in xrange(0, board_length):
			if board[i][j] == GLOBALS.BLOCK_CODES['safe']:
				click(j,i)
				was_clicked = True
	return was_clicked

solver = Solver()
counter = 0


"""Remaining->"""
while mines_remaining != 0:
	getInputOfBlocks()
	mines_remaining = GLOBALS.TOTAL_MINES_REMAINING
	while True:
		flag = False
		for val in GLOBALS.BLOCK_NUMBERS:
			print "Iterating for val = {0}".format(val)
			position = positions[str(val)]
			for coordinates in position:
				blocks_coordinates, counts = setProbabilityFlag(coordinates[0], coordinates[1])
				s = "{0}, {1} ->".format((coordinates[0], coordinates[1]),val)
				print s,
				print blocks_coordinates, counts
				if counts['mines_count'] == val and counts['blank_count'] > 0:
					print "marking safe the coordinates: {0}".format(blocks_coordinates)
					status = solver.mark_all(board, blocks_coordinates, GLOBALS.BLOCK_CODES['safe'])
					if status:
						flag = True
				elif counts['blank_count'] <= val-counts['mines_count']:
					# All the mines
					status = solver.mark_all(board, blocks_coordinates, GLOBALS.BLOCK_CODES['mines'])
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
time.sleep(0.2)
if not is_game_finished():
	# If the message box that says that the game is finished has not yet come, then mark all the mines
	for i in xrange(0,8):
		for j in xrange(0,8):
			if board[i][j] == -100:
				click(j,i,3)