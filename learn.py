import sys
import collections
import operator
import numpy
import unittest
import random
import copy
from unittest import TestCase


def clearBoard():
	for i in range(4):
		for j in range(4):
			for k in range(4):
				board[i][j][k] = ''


def resetPotentialMoves():
	for i in range(4):
		for j in range(4):
			for k in range(4):
				coord = (i, j, k)
				potentialMoves[coord] = utility[i][j][k]


board = numpy.chararray((4, 4, 4))
clearBoard()
utility = numpy.zeros((4, 4, 4))
# board[row][col][floor]

p1, p2 = b'X', b'O'
explorationRate = 0.25
potentialMoves = {}
resetPotentialMoves()
p1moves = collections.OrderedDict()
p2moves = collections.OrderedDict()
dangerZones = []
winZones = []


def learn(loops):
	global explorationRate
	clearBoard()
	maxUtility = (2, 2, 2)  # maxUtility are the coordinates of the best utility value
	for loop in range(loops):
		while True:

			if numpy.random.uniform(0, 1) <= explorationRate:
				# p1 chooses move based on probabilities of the board
				p1move = potentialMoves.pop(maxUtility)  # p1move is the best utility value
			else:
				maxUtility = random.choice(list(potentialMoves))  # randomly chooses a move to make
				p1move = potentialMoves.pop(maxUtility)
				explorationRate *= 0.95

			p1moves[maxUtility] = p1move  # add to list of player 1's moves in the form (key:coordinate, value:utility)
			board[maxUtility[0]][maxUtility[1]][maxUtility[2]] = p1

			if winCheck(maxUtility, p1, 4) == 1:
				calculate(p1moves)
				break

			if potentialMoves:
				maxUtility = max(potentialMoves.items(), key=operator.itemgetter(1))[0]
			else:
				break

			if numpy.random.uniform(0, 1) <= explorationRate:
				p2move = potentialMoves.pop(maxUtility)
			else:
				maxUtility = random.choice(list(potentialMoves))
				p2move = potentialMoves.pop(maxUtility)
				explorationRate *= 0.95

			p2moves[maxUtility] = p2move  # add to list of player 2's moves in the form (key:coordinate, value:utility)
			board[maxUtility[0]][maxUtility[1]][maxUtility[2]] = p2

			if winCheck(maxUtility, p2, 4) == 1:
				calculate(p2moves)
				break

			if potentialMoves:
				maxUtility = max(potentialMoves.items(), key=operator.itemgetter(1))[0]
			else:
				break

		clearBoard()
		resetPotentialMoves()


def play():
	learn(2000)
	while True:

		if winZones:
			player = winZones.pop(0)
		elif dangerZones:
			player = dangerZones.pop(0)
		else:
			player = max(potentialMoves.items(), key=operator.itemgetter(1))[0]
		potentialMoves.pop(player)
		board[player[0]][player[1]][player[2]] = p1
		print(board)
		print(player)
		print(winZones)
		print(dangerZones)

		if winCheck(player, p1, 4) == 1:
			print("AI wins")
			break
		opponent = input('Enter coordinates of next move: ')
		opponent = int(opponent[0]), int(opponent[1]), int(opponent[2])
		board[int(opponent[0])][int(opponent[1])][int(opponent[2])] = p2
		potentialMoves.pop(opponent)
		if winCheck(opponent, p2, 4) == 1:
			print("human wins")
			break

		strategyCheck(player, p1, 3, winZones)
		strategyCheck(opponent, p2, 3, dangerZones)
		if len(potentialMoves) <= 39:
			strategyCheck(player, p1, 2, winZones)
			strategyCheck(opponent, p2, 2, dangerZones)


def normalize(passedUtility):
	sum = numpy.sum(passedUtility)
	sum /= 64
	for i in range(4):
		for j in range(4):
			for k in range(4):
				passedUtility[i][j][k] /= sum


def calculate(winner):
	# match everything in the winner's dict to the board, increase
	# do the same with the loser
	# update the potentialMoves list
	qMax = 1
	alpha = 0.4
	while not len(winner.keys()) == 0:
		x, y, z = list(winner.keys())[-1][0], list(winner.keys())[-1][1], list(winner.keys())[-1][2]
		utility[x][y][z] += alpha * qMax  # update utility function with Q-value
		qMax = qMax * alpha
		potentialMoves[(x, y, z)] = utility[x][y][z]  # update potentialMoves (re-set)
		del winner[(x, y, z)]
	p1moves.clear()
	p2moves.clear()


def strategyCheck(move, player, check, arr):
	row, col, floor = move[0], move[1], move[2]

	r = collections.Counter([board[i][col][floor] for i in range(4)])
	if r[player] == check:
		for j in range(4):
			if board[j][col][floor] == '':
				arr.append((j, col, floor))

	c = collections.Counter([board[row][i][floor] for i in range(4)])
	if c[player] == check:
		for j in range(4):
			if board[row][j][floor] == '':
				arr.append((row, j, floor))
	f = collections.Counter([board[row][col][i] for i in range(4)])
	if f[player] == check:
		for j in range(4):
			if board[row][col][j] == '':
				arr.append((row, col, j))

	# check diagonals
	if row - col == 0:
		d0 = collections.Counter([board[i][i][floor] for i in range(4)])
		if d0[player] == check:
			for j in range(4):
				if board[j][j][floor] == '':
					arr.append((j, j, floor))
	elif row + col == 3:
		d0 = collections.Counter([board[i][3 - i][floor] for i in range(4)])
		if d0[player] == check:
			for j in range(4):
				if board[j][3-j][floor] == '':
					arr.append((j, 3-j, floor))

	if col - floor == 0:
		d1 = collections.Counter([board[row][i][i] for i in range(4)])
		if d1[player] == check:
			for j in range(4):
				if board[row][j][j] == '':
					arr.append((row, j, j))
	elif col + floor == 3:
		d1 = collections.Counter([board[row][i][3 - i] for i in range(4)])
		if d1[player] == check:
			for j in range(4):
				if board[row][j][3-j] == '':
					arr.append((row, j, 3-j))

	if floor - row == 0:
		d2 = collections.Counter([board[i][col][i] for i in range(4)])
		if d2[player] == check:
			for j in range(4):
				if board[j][col][j] == '':
					arr.append((j, col, j))
	elif floor + row == 3:
		d2 = collections.Counter([board[i][col][3 - i] for i in range(4)])
		if d2[player] == check:
			for j in range(4):
				if board[j][col][3-j] == '':
					arr.append((j, col, 3-j))

	return 0


def winCheck(move, player, check):
	# 0 is no win, 1 is yes win, -1 is 3-in-a-row
	row, col, floor = move[0], move[1], move[2]
	r = collections.Counter([board[i][col][floor] for i in range(4)])
	if r[player] == check:
		return 1
	c = collections.Counter([board[row][i][floor] for i in range(4)])
	if c[player] == check:
		return 1
	f = collections.Counter([board[row][col][i]for i in range(4)])
	if f[player] == check:
		return 1

	# check diagonals
	if row - col == 0:
		d0 = collections.Counter([board[i][i][floor] for i in range(4)])
		if d0[player] == check:
			return 1
	elif row + col == 3:
		d0 = collections.Counter([board[i][3 - i][floor] for i in range(4)])
		if d0[player] == check:
			return 1

	if col - floor == 0:
		d1 = collections.Counter([board[row][i][i] for i in range(4)])
		if d1[player] == check:
			return 1
	elif col + floor == 3:
		d1 = collections.Counter([board[row][i][3 - i] for i in range(4)])
		if d1[player] == check:
			return 1

	if floor - row == 0:
		d2 = collections.Counter([board[i][col][i] for i in range(4)])
		if d2[player] == check:
			return 1
	elif floor + row == 3:
		d2 = collections.Counter([board[i][col][3 - i] for i in range(4)])
		if d2[player] == check:
			return 1

	return 0


# -------------- actual script run -------------- #
# learn(int(sys.argv[1]))
# utility1 = copy.deepcopy(utility)
# normalize(utility1)
#
# learn(int(sys.argv[2]) - int(sys.argv[1]))
# utility2 = copy.deepcopy(utility)
# normalize(utility2)
#
# learn(int(sys.argv[3]) - int(sys.argv[2]) - int(sys.argv[1]))
# utility3 = copy.deepcopy(utility)
# normalize(utility3)

play()


# -------------------TESTS-------------------
# class TestLearn(TestCase):
# 	# Use the following command in the terminal to view the individual test results...
# 	# python3 -m unittest -v learn.py
#
#
#
# 	#------------------LEARN TESTS---------------------
#
# 	def test_learn_run(self):
# 		learn(1000)
# 		print(utility)
# 		self.assertFalse(numpy.all(utility == 0))
#
# 	#------------------WINCHECK TESTS------------------
# 	def test_winCheck_floor(self):
# 		clearBoard()
# 		board[0][0][0] = p1
# 		board[0][0][1] = p1
# 		board[0][0][2] = p1
# 		board[0][0][3] = p1
# 		move = 0, 0, 3
# 		result = winCheck(move, p1, 4)
# 		self.assertEqual(result, 1)
#
# 	def test_winCheck_column(self):
# 		clearBoard()
# 		board[0][0][0] = p1
# 		board[0][1][0] = p1
# 		board[0][2][0] = p1
# 		board[0][3][0] = p1
# 		move = 0, 3, 0
# 		result = winCheck(move, p1, 4)
# 		self.assertEqual(result, 1)
#
# 	def test_winCheck_row(self):
# 		clearBoard()
# 		board[0][0][0] = p1
# 		board[1][0][0] = p1
# 		board[2][0][0] = p1
# 		board[3][0][0] = p1
# 		move = 3, 0, 0
# 		result = winCheck(move, p1, 4)
# 		self.assertEqual(result, 1)
#
# 	def test_winCheck_diagonal(self):
# 		clearBoard()
# 		board[0][0][0] = p1
# 		board[0][1][1] = p1
# 		board[0][2][2] = p1
# 		board[0][3][3] = p1
# 		move = 0, 3, 3
# 		result = winCheck(move, p1, 4)
# 		self.assertEqual(result, 1)
#
# 	def test_winCheck_no_win(self):
# 		clearBoard()
# 		move = 0, 0, 0
# 		result = winCheck(move, p1, 4)
# 		self.assertEqual(result, 0)

if __name__ == '__main__':
	unittest.main()
