import sys
import collections
import numpy
import unittest
from unittest import TestCase

board = numpy.zeros((4, 4, 4))
# board = [[[0] * 4] * 4] * 4
# board[row][col][floor]

potential_moves = {}
moves = {}

for i in range(4):
    for j in range(4):
        for k in range(4):
            coord = (i, j, k)
            potential_moves[coord] = 0


def clearBoard():
    board * 0


def winCheck(move, player):
    # 0 is no win, 1 is yes win

    row, col, floor = move[0], move[1], move[2]

    r = collections.Counter([board[i][col][floor] for i in range(4)])
    if r[player] == 4:
        return 1
    c = collections.Counter([board[row][i][floor] for i in range(4)])
    if c[player] == 4:
        return 1
    f = collections.Counter([board[row][col][i] for i in range(4)])
    if f[player] == 4:
        return 1

    # check diagonals
    if row - col == 0:
        d0 = collections.Counter([board[i][i][floor] for i in range(4)])
    elif row + col == 3:
        d0 = collections.Counter([board[i][3 - i][floor] for i in range(4)])
    if d0[player] == 4:
        return 1

    if col - floor == 0:
        d1 = collections.Counter([board[row][i][i] for i in range(4)])
    elif col + floor == 3:
        d1 = collections.Counter([board[row][i][3 - i] for i in range(4)])
    if d1[player] == 4:
        return 1

    if floor - row == 0:
        d2 = collections.Counter([board[i][col][i] for i in range(4)])
    elif floor + row == 3:
        d2 = collections.Counter([board[i][col][3 - i] for i in range(4)])
    if d2[player] == 4:
        return 1

    return 0


# -------------------TESTS-------------------
class TestLearn(TestCase):

    def test_winCheck_floor(self):
        clearBoard()
        board[0][0][0] = 1
        board[0][0][1] = 1
        board[0][0][2] = 1
        board[0][0][3] = 1
        move = 0, 0, 3
        result = winCheck(move, 1)
        self.assertEqual(result, 1)

    def test_winCheck_column(self):
        clearBoard()
        board[0][0][0] = 1
        board[0][1][0] = 1
        board[0][2][0] = 1
        board[0][3][0] = 1
        move = 0, 3, 0
        result = winCheck(move, 1)
        self.assertEqual(result, 1)

    def test_winCheck_row(self):
        clearBoard()
        board[0][0][0] = 1
        board[1][0][0] = 1
        board[2][0][0] = 1
        board[3][0][0] = 1
        move = 3, 0, 0
        result = winCheck(move, 1)
        self.assertEqual(result, 1)

    def test_winCheck_diagonal(self):
        clearBoard()
        board[0][0][0] = 1
        board[0][1][1] = 1
        board[0][2][2] = 1
        board[0][3][3] = 1
        move = 0, 3, 3
        result = winCheck(move, 1)
        self.assertEqual(result, 1)

    def test_winCheck_no_win(self):
        clearBoard()
        move = 0, 0, 0
        result = winCheck(move, 1)
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
