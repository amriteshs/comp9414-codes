#!/usr/bin/python3
# Sample starter bot by Zac Partridge
# 06/04/19
# Feel free to use this and modify it however you wish

import socket
import sys
from copy import deepcopy
from math import inf

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
curr = None     # no board selected initially
depth = 4       # minimax depth


class Board(object):
    def __init__(self, player):
        self.player = player    # current player
        self.curr = 0           # current board
        self.xscore = 0         # current player's heuristic X score
        self.oscore = 0         # current player's heuristic O score
        self.boards = [['.' for _ in range(1, 10)] for _ in range(1, 10)]   # initialize board
        self.winning_triads = [                 # winning outcomes
                                [0, 1, 2],
                                [3, 4, 5],
                                [6, 7, 8],
                                [0, 3, 6],
                                [1, 4, 7],
                                [2, 5, 8],
                                [0, 4, 8],
                                [2, 4, 6]
                            ]

    # add a move to the current board for the player
    def place(self, turn, curr, move):
        if curr is None:
            curr = self.curr

        # recalculate X score and O score for move according to heuristic
        for i in self.winning_triads:
            seqx = 0
            seqo = 0

            for j in i:
                if self.boards[curr - 1][j] == 'X':
                    seqx += 1
                    seqo -= 3
                elif self.boards[curr - 1][j] == 'O':
                    seqx -= 3
                    seqo += 1

            if seqx == 1:
                self.xscore -= 1
            elif seqx == 2:
                self.xscore -= 10
            elif seqx == 3:
                self.xscore -= 10000

            if seqo == 1:
                self.oscore -= 1
            elif seqo == 2:
                self.oscore -= 10
            elif seqo == 3:
                self.oscore -= 10000

        if turn == 1:
            self.boards[curr - 1][move - 1] = self.player
        else:
            if self.player == 'O':
                self.boards[curr - 1][move - 1] = 'X'
            elif self.player == 'X':
                self.boards[curr - 1][move - 1] = 'O'

        for i in self.winning_triads:
            seqx = 0
            seqo = 0

            for j in i:
                if self.boards[curr - 1][j] == 'X':
                    seqx += 1
                    seqo -= 3
                elif self.boards[curr - 1][j] == 'O':
                    seqx -= 3
                    seqo += 1

            if seqx == 1:
                self.xscore += 1
            elif seqx == 2:
                self.xscore += 10
            elif seqx == 3:
                self.xscore += 10000

            if seqo == 1:
                self.oscore += 1
            elif seqo == 2:
                self.oscore += 10
            elif seqo == 3:
                self.oscore += 10000

        # reset current board to move
        self.curr = move

    # find board objects directly obtainable from current board
    def next(self, turn):
        # list of next boards
        nextb = []

        for i in range(9):
            if self.boards[self.curr - 1][i] not in ('O', 'X'):
                # copy current board to new board
                newb = Board(deepcopy(self.player))
                newb.boards = deepcopy(self.boards)
                newb.xscore = deepcopy(self.xscore)
                newb.oscore = deepcopy(self.oscore)
                newb.curr = deepcopy(self.curr)
                newb.winning_triads = deepcopy(self.winning_triads)

                # add move to new board according to player's turn
                if turn == 1:
                    newb.place(2, self.curr, i + 1)
                else:
                    newb.place(1, self.curr, i + 1)

                # append new board to list
                nextb.append(newb)

        return nextb


# generate tree for current board with next possible boards as children nodes
def generate_tree(board, depth, turn):
    if not depth:
        return board, []

    tree = board, []

    # recursively generate children boards and append to tree
    for i in board.next(turn):
        if turn == 1:
            tree[1].append(generate_tree(i, depth - 1, 2))
        else:
            tree[1].append(generate_tree(i, depth - 1, 1))

    return tree


# generate an alpha-beta pruned tree for current board object
def play(depth):
    global curr

    best_board = None
    best_score = -1 * (10 ** 10)

    # generate tree with other player as root
    tree = generate_tree(curr, depth, 2)

    # set player 1 as max for minimax algorithm
    def player1(tree, alpha, beta, player):
        tree[0].player = player

        if not len(tree[1]):
            tscore = tree[0].xscore - tree[0].oscore

            if tree[0].player == 'O':
                return -tscore

            return tscore

        for node in tree[1]:
            alpha = max(alpha, player2(node, alpha, beta, tree[0].player))

            # if alpha < beta, prune subtree
            if alpha < beta:
                return alpha

        return alpha

    # set player 2 as min for minimax algorithm
    def player2(tree, alpha, beta, player):
        tree[0].player = player

        if not len(tree[1]):
            tscore = tree[0].xscore - tree[0].oscore

            if tree[0].player == 'O':
                return -tscore

            return tscore

        for node in tree[1]:
            beta = min(beta, player1(node, alpha, beta, tree[0].player))

            # if alpha < beta, prune subtree
            if alpha < beta:
                return beta

        return beta

    # find child node for board tree whose heuristic gives best probability of winning
    for node in tree[1]:
        # alpha set to -infinity initially
        # beta set to +infinity initially
        score = player1(node, -inf, inf, curr.player)
        if best_score < score:
            best_board = node[0]
            best_score = score

    # add best move to board and return
    curr.place(1, None, best_board.curr)

    return best_board.curr


# print a row
# This is just ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    # The marking script doesn't seem to like this either, so just take it out to submit
    print('', board[a][i], board[a][j], board[a][k], end=' | ')
    print(board[b][i], board[b][j], board[b][k], end=' | ')
    print(board[c][i], board[c][j], board[c][k])


# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(board, 1, 2, 3, 1, 2, 3)
    print_board_row(board, 1, 2, 3, 4, 5, 6)
    print_board_row(board, 1, 2, 3, 7, 8, 9)
    print(' ------+-------+------')
    print_board_row(board, 4, 5, 6, 1, 2, 3)
    print_board_row(board, 4, 5, 6, 4, 5, 6)
    print_board_row(board, 4, 5, 6, 7, 8, 9)
    print(' ------+-------+------')
    print_board_row(board, 7, 8, 9, 1, 2, 3)
    print_board_row(board, 7, 8, 9, 4, 5, 6)
    print_board_row(board, 7, 8, 9, 7, 8, 9)
    print()


# read what the server sent us and
# only parses the strings that are necessary
def parse(string, depth=3):
    global curr

    if '(' in string:
        command, args = string.split('(')
        args = args.split(')')[0]
        args = args.split(',')
    else:
        command, args = string, []

    if command == 'start':
        # set player to O or X
        if args[0] == 'o':
            curr = Board('O')
        else:
            curr = Board('X')

    if command == 'second_move':
        curr.place(2, int(args[0]), int(args[1]))
        return play(depth)

    elif command == 'third_move':
        # add move to board for player 1
        curr.place(1, int(args[0]), int(args[1]))
        # add move to board for player 2
        curr.place(2, curr.curr, int(args[2]))
        return play(depth)

    elif command == 'next_move':
        # add move to board for player 2
        curr.place(2, curr.curr, int(args[0]))
        return play(depth)

    elif command == 'last_move':
        # add move to board for player 2
        curr.place(2, curr.curr, int(args[0]))

    elif command == 'draw':
        print('It\'s a draw!!')
        return -1

    elif command == 'win':
        print('Yay!! We win!! :)')
        return -1

    elif command == 'loss':
        print('We lost :(')
        return -1

    elif command == 'end':
        return -1

    return 0


# connect to socket
def main():
    # global depth

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2])  # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()

        if not text:
            continue

        for line in text.split('\n'):
            response = parse(line, depth)

            if response == -1:
                s.close()
                return

            elif response > 0:
                s.sendall((str(response) + '\n').encode())


if __name__ == '__main__':
    main()
