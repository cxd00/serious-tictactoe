import sys
import collections
from unittest import TestCase

board = [[[0] * 4] * 4] * 4
probabilities = [[[1] * 4] * 4] * 4
# board[row][col][floor]

potentialMoves = {}
p1moves = {}
p2moves = {}

for i in range(4):
    for j in range(4):
        for k in range(4):
            coord = (i, j, k)
            potentialMoves[coord] = 0


def printBoard():
    for x in range(len(board)):
        print(board[x])


def learn(loops):
    # p1 chooses random move based on probabilities of the board
        # order potential_moves, take from top
        # add to p1moves
        # wincheck
    # p2 chooses next move
        # take next move off of potential_moves, add to p2moves
        # wincheck
    # call calculate


def calculate():
    # match everything in the winner's dict to the board, increase
    # do the same with the loser
    # update the potentialMoves list


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
    def test_winCheck(self):
        printBoard()
        move = 0, 0, 3
        result = winCheck(move, 1)
        self.assertEqual(result, 0)
