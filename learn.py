import sys
import collections
import operator
import numpy
import unittest
from unittest import TestCase

board = numpy.chararray((4, 4, 4))
utility = numpy.zeros((4, 4, 4))
# board[row][col][floor]

potentialMoves = {}
p1moves = collections.OrderedDict()
p2moves = collections.OrderedDict()

for i in range(4):
	for j in range(4):
		for k in range(4):
			coord = (i, j, k)
			potentialMoves[coord] = 0


def learn(loops):
	board = numpy.chararray((4, 4, 4))
	p1, p2 = 'X', 'O'
	maxUtility = (2, 2, 2)  # maxUtility are the coordinates of the best utility value
	for loop in range(loops):
		# p1 chooses move based on probabilities of the board
		p1move = potentialMoves.pop(maxUtility)  # p1move is the best utility value
		p1moves[maxUtility] = p1move  # add to list of player 1's moves in the form (key:coordinate, value:utility)
		board[maxUtility[0]][maxUtility[1]][maxUtility[2]] = p1
		if winCheck(maxUtility, p1) == 1:
			calculate(p1moves)
		maxUtility = max(potentialMoves.items(), key=operator.itemgetter(1))[0]

		p2move = potentialMoves.pop(maxUtility)  # p1move is the best utility value
		p2moves[maxUtility] = p2move  # add to list of player 2's moves in the form (key:coordinate, value:utility)
		board[maxUtility[0]][maxUtility[1]][maxUtility[2]] = p2
		if winCheck(maxUtility, p2) == 1:
			calculate(p2moves)
		maxUtility = max(potentialMoves.items(), key=operator.itemgetter(1))[0]
		print(board)

def calculate(winner):
	# match everything in the winner's dict to the board, increase
	# do the same with the loser
	# update the potentialMoves list
	qMax = 1
	while not len(winner.keys()) == 0:
		x, y, z = winner.keys()[-1][0], winner.keys()[-1][1], winner.keys()[-1][2]
		utility[x][y][z] += 0.99 * qMax  # update utility function with Q-value
		potentialMoves[(x, y, z)] = utility[x][y][z]  # update potentialMoves (re-set)
		print(utility)
		del winner[(x, y, z)]
	p1moves = {}
	p2moves = {}


def winCheck(move, player):
	# 0 is no win, 1 is yes win
	row, col, floor = move[0], move[1], move[2]
	r = collections.Counter([board[i][col][floor] for i in range(4)])
	if r[player] == 4:
		return 1
	c = collections.Counter([board[row][i][floor] for i in range(4)])
	if c[player] == 4:
		return 1
	f = collections.Counter([board[row][col][i]for i in range(4)])
	if f[player] == 4:
		return 1

	# check diagonals
	if row - col == 0:
		d0 = collections.Counter([board[i][i][floor] for i in range(4)])
		if d0[player] == 4:
			return 1
	elif row + col == 3:
		d0 = collections.Counter([board[i][3 - i][floor] for i in range(4)])
		if d0[player] == 4:
			return 1

	if col - floor == 0:
		d1 = collections.Counter([board[row][i][i] for i in range(4)])
		if d1[player] == 4:
			return 1
	elif col + floor == 3:
		d1 = collections.Counter([board[row][i][3 - i] for i in range(4)])
		if d1[player] == 4:
			return 1

	if floor - row == 0:
		d2 = collections.Counter([board[i][col][i] for i in range(4)])
		if d2[player] == 4:
			return 1
	elif floor + row == 3:
		d2 = collections.Counter([board[i][col][3 - i] for i in range(4)])
		if d2[player] == 4:
			return 1

	return 0


# -------------------TESTS-------------------
class TestLearn(TestCase):
	# Use the following command in the terminal to view the individual test results...
	# python -m unittest -v learn.py

	def clearBoard(self):
		for i in range(4):
			for j in range(4):
				for k in range(4):
					board[i][j][k] = ''


	#------------------LEARN TESTS---------------------

	def test_learn_run(self):
		learn(10)
		self.assertFalse(numpy.any(utility == 0))

	#------------------WINCHECK TESTS------------------
	def test_winCheck_floor(self):
		self.clearBoard()
		board[0][0][0] = 'X'
		board[0][0][1] = 'X'
		board[0][0][2] = 'X'
		board[0][0][3] = 'X'
		move = 0, 0, 3
		result = winCheck(move, 'X')
		self.assertEqual(result, 1)

	def test_winCheck_column(self):
		self.clearBoard()
		board[0][0][0] = 'X'
		board[0][1][0] = 'X'
		board[0][2][0] = 'X'
		board[0][3][0] = 'X'
		move = 0, 3, 0
		result = winCheck(move, 'X')
		self.assertEqual(result, 1)

	def test_winCheck_row(self):
		self.clearBoard()
		board[0][0][0] = 'X'
		board[1][0][0] = 'X'
		board[2][0][0] = 'X'
		board[3][0][0] = 'X'
		move = 3, 0, 0
		result = winCheck(move, 'X')
		self.assertEqual(result, 1)

	def test_winCheck_diagonal(self):
		self.clearBoard()
		board[0][0][0] = 'X'
		board[0][1][1] = 'X'
		board[0][2][2] = 'X'
		board[0][3][3] = 'X'
		move = 0, 3, 3
		result = winCheck(move, "X")
		self.assertEqual(result, 1)

	def test_winCheck_no_win(self):
		self.clearBoard()
		move = 0, 0, 0
		result = winCheck(move, 'X')
		print(board)
		self.assertEqual(result, 0)


if __name__ == '__main__':
	unittest.main()
