print "Instructions: "
print "-1: Block not yet revealed."
print "0: Block revealed and is null"
print "1,2,3,4,5: Numbers that are opened"

POSSIBLE_NUMBERS = [-1, 0, 1, 2, 3, 4, 5]
board = []
positions = {}

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

			if board[x_final][y_final] == GLOBALS['mines']:
				mines_count += 1
			elif board[x_final][y_final] == GLOBALS['safe'] :
				safe_count += 1
			elif inrange(x+xdiff,7) and inrange(y+ydiff,7) and board[x_final][y_final] == GLOBALS['blank']:
				coordinates.append((x+xdiff, y+ydiff))
				blank_count += 1
				# print (x+xdiff,y+ydiff)

	return coordinates, { 'blank_count': blank_count, 'safe_count': safe_count, 'mines_count': mines_count }
	"""
		The whole target of the above code was to go to the generate all the neighbouring places of a given center coordinate
		((1,1) in this case)
	"""

for i in POSSIBLE_NUMBERS:
	positions[str(i)] = []

for i in xrange(0,8):
	a = raw_input("Enter the row number {0}: ".format(i)).strip()
	a = map(int, a.split(' '))
	for j in xrange(0,8):
		positions[str(a[j])].append((i,j))
	# print position
	board.append(a)

current = 1
position = positions[str(current)]
for coordinates in position:
	blocks_coordinates, counts = setProbabilityFlag(coordinates[0], coordinates[1])
	print blocks_coordinates, counts