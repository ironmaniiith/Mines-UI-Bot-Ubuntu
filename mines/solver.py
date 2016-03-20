import os, time
import giveDimensions
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


def getInputOfBlocks():
	board = []
	positions = {}

	for i in POSSIBLE_NUMBERS:
		positions[str(i)] = []

	for i in xrange(0,8):
		a = raw_input().strip()
		a = map(int, a.split(' '))
		for j in xrange(0,8):
			positions[str(a[j])].append((i,j))
		# print position
		board.append(a)

def click(i,j):
	os.system("xdotool mousemove {0} {1} click 1".format(location[i][j]))
	time.sleep(0.5)

def clickOnSafeFlags():
	for i in xrange(0,board_length):
		for j in xrange(0, board_length):
			if board_length[i][j] == GLOBALS['safe']:
				click(i,j)
	return

while TOTAL_MINES_REMAINING != 0:
	getInputOfBlocks()
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
			print "Breaking at i = {0} more information needed for proceeding".format(i)
			clickOnSafeFlags()
			break