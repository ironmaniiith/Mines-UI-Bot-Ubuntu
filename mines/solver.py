#!/usr/bin/python
from modules import *
import GLOBALS
import giveDimensions
import findNumbers, findOpened, findImage

board = []
positions = {}
mines_remaining = GLOBALS.TOTAL_MINES_REMAINING

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
	counts = {'blank': 0, 'mines': 0, 'safe': 0}

	for xdiff in xrange(-1,2):
		for ydiff in xrange(-1,2,2-xdiff%2):
			x_final = x + xdiff
			y_final = y + ydiff

			if inrange(x_final,8) and inrange(y_final, 8):
				if board[x_final][y_final] == GLOBALS.BLOCK_CODES['mines']:
					counts['mines'] += 1
				elif board[x_final][y_final] == GLOBALS.BLOCK_CODES['safe']:
					counts['safe'] += 1
				elif board[x_final][y_final] == GLOBALS.BLOCK_CODES['blank']:
					coordinates.append((x+xdiff, y+ydiff))
					counts['blank'] += 1

	return coordinates, counts
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

def is_game_finished():
	coordinates, x = findImage.main('finished') # finished.png is the image when the game is finished
	if len(coordinates):
		exit(0)
	return False

def get_cropped_image():
	os.system('scrot -z -q 100 fullScreen.png')
	os.system('convert -crop 670x670+260+85 fullScreen.png cropped.png')

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
	get_cropped_image()
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

def check_end():
	time.sleep(0.3)
	get_cropped_image()
	if not is_game_finished():
		# If the message box that says that the game is finished has not yet come, then mark all the mines
		click_type = 3 # Right click to mark the mines
		for i in xrange(0, GLOBALS.number_of_blocks):
			for j in xrange(0, GLOBALS.number_of_blocks):
				if board[i][j] == GLOBALS.BLOCK_CODES['mines']:
					click(j,i,click_type)

solver = Solver()
counter = 0

while mines_remaining != 0:
	getInputOfBlocks()
	mines_remaining = GLOBALS.TOTAL_MINES_REMAINING
	while True:
		flag = False
		
		for val in GLOBALS.BLOCK_NUMBERS:
			position = positions[str(val)]
			for coordinates in position:
				blocks_coordinates, counts = setProbabilityFlag(coordinates[0], coordinates[1])

				mark = None
				if (counts['mines'] == val and counts['blank'] > 0):
					mark = GLOBALS.BLOCK_CODES['safe']
				elif (counts['blank'] <= val-counts['mines']):
					mark = GLOBALS.BLOCK_CODES['mines']
				
				if mark != None:
					status = solver.mark_all(board, blocks_coordinates, mark)
					if status:
						flag = True

		if not flag:
			was_clicked = clickOnSafeFlags(GLOBALS.number_of_blocks)
			if not was_clicked:
				counter += 1
			if counter == 2:
				counter = 0
				clickRandom()
			break

print 'Game ended, all flags found'
check_end()