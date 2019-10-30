import sys

runs = sys.argv[1]
board = [[[0]*4]*4]*4

potential_moves = {}
moves = {}

for i in range(4):
    for j in range(4):
        for k in range(4):
            coord = [i, j, k]
            potential_moves[coord] = 0


def winCheck(move, player, count):
    row, col, floor = move[0], move[1], move[2]
    if -1 in {row, col, floor} or 4 in {row, col, floor}:
        return count
    if board[row][col][floor] == player:
        winCheck([row+1, col, floor], player, count+1)
        winCheck([row-1, col, floor], player, count+1)
        winCheck([row, col+1, floor], player, count+1)
        winCheck([row, col-1, floor], player, count+1)
        winCheck([row, col, floor+1], player, count+1)
        winCheck([row, col, floor-1], player, count+1)
        # if row/col == 1:
        #     winCheck([row + 1, col, floor], player, count+1)
        # if col/floor == 1:
        #     winCheck([row + 1, col, floor], player, count+1)
        # if row/floor == 1:
        #     winCheck([row + 1, col, floor], player, count+1)


