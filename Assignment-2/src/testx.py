#!/usr/bin/python3
# Sample starter bot by Zac Partridge
# 06/04/19
# Feel free to use this and modify it however you wish

import socket
import sys
import copy
from math import inf

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
# boards = np.zeros((10, 10), dtype='int8')
boards = [[0] * 10] * 10
curr = 0  # this is the current board to play in
curr_board_obj = None
MINIMAX_DEPTH = 4


class Board(object):
    def __init__(self, player=''):
        self.player = player
        self.curr_board_obj = 0
        self.last_move = 0
        self.last_board = 0
        self.boards = [['.' for _ in range(1, 10)] for j in range(1, 10)]
        self.x_score = 0
        self.o_score = 0

    def __copy__(self):
        board_copy = Board(copy.deepcopy(self.player))
        board_copy.boards = copy.deepcopy(self.boards)
        board_copy.last_move = copy.deepcopy(self.last_move)
        board_copy.x_score = copy.deepcopy(self.x_score)
        board_copy.o_score = copy.deepcopy(self.o_score)
        board_copy.curr_board_obj = copy.deepcopy(self.curr_board_obj)
        return board_copy

    def place(self, move, curr_board_obj=None, turn=1):
        """Add a move to the board."""
        if curr_board_obj is None:
            curr_board_obj = self.curr_board_obj

        previous_x = self.calculate_board_score(curr_board_obj, 'X')
        previous_o = self.calculate_board_score(curr_board_obj, 'O')

        if turn == 1:
            self.boards[curr_board_obj - 1][move - 1] = self.player
        elif self.player == 'X':
            self.boards[curr_board_obj - 1][move - 1] = 'O'
        elif self.player == 'O':
            self.boards[curr_board_obj - 1][move - 1] = 'X'

        new_x = self.calculate_board_score(curr_board_obj, 'X')
        new_o = self.calculate_board_score(curr_board_obj, 'O')

        self.x_score = self.x_score - previous_x + new_x
        self.o_score = self.o_score - previous_o + new_o
        self.last_move = move
        self.last_board = curr_board_obj
        self.curr_board_obj = move

        # place(self.last_board, self.last_move, 1)

    def winning_triads(self):
        winlines = []

        for a in range(0, 3):
            winlines.append(range(a * 3, a * 3 + 3))
            winlines.append(range(a, 9, 3))

        winlines.append(range(2, 8, 2))
        winlines.append(range(0, 9, 4))

        return winlines

    def calculate_board_score(self, curr_board_obj, player):
        score = 0

        win_outcomes = self.winning_triads()

        for i in win_outcomes:
            num = 0
            for j in i:
                if self.boards[curr_board_obj - 1][j] == player:
                    num += 1
                elif self.boards[curr_board_obj - 1][j] != '.':
                    num -= 3

            if num == 3:
                score += (10 ** 10)
            elif num == 2:
                score += 10
            elif num == 1:
                score += 1

        return score

    def is_legal(self, move):
        return

    def get_score(self):
        if self.player == 'X':
            return self.x_score - self.o_score

        return self.o_score - self.x_score

    def next_boards(self, turn):
        new_boards = []

        for i in range(1, 10):
            if self.boards[self.curr_board_obj - 1][i - 1] not in ('O', 'X'):
                new_board = copy.copy(self)

                if turn == 1:
                    new_board.place(i, self.curr_board_obj, 2)
                else:
                    new_board.place(i, self.curr_board_obj, 1)

                new_boards.append(new_board)

        return new_boards


class Tree(object):
    """A Tree with a list of Trees as children
        and a value (a Board)"""

    def __init__(self, value=None):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children.extend(children)


def generate_tree(curr_board_obj, depth, turn):
    states = curr_board_obj, []

    if not depth:
        return states

    for next_board in curr_board_obj.next_boards(turn):
        if turn == 1:
            states[1].append(generate_tree(next_board, depth - 1, 2))
        else:
            states[1].append(generate_tree(next_board, depth - 1, 1))

    return states


def play(depth):
    global curr_board_obj

    move_tree = generate_tree(curr_board_obj, depth, 2)

    best_board = None
    best_score = -1 * (10 ** 10)

    a = -inf
    b = inf

    def max_score(tree, a, b, original_player):
        """Perform a minimax with alpha-beta pruning
            on a tree of Board objects to return the
            score for the given board"""
        tree[0].player = original_player
        if len(tree[1]) == 0:
            return tree[0].get_score()

        for child in tree[1]:
            a = max(a, min_score(child, a, b, original_player))
            # child_score = random.randint(-100000, 100000)
            if b <= a:
                break

        return a

    def min_score(tree, a, b, original_player):
        tree[0].player = original_player
        if len(tree[1]) == 0:
            return tree[0].get_score()

        for child in tree[1]:
            b = min(b, max_score(child, a, b, original_player))
            if b <= a:
                break

        return b

    for child in move_tree[1]:
        child_score = max_score(child, a, b, curr_board_obj.player)
        if child_score > best_score:
            best_board = child[0]
            best_score = child_score

    curr_board_obj.place(best_board.last_move)

    return best_board.curr_board_obj


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


# choose a move to play
# def play():
#     # n = AlphaBeta(boards, curr).minimax()
#     # place(curr, n, 1)
#     # print(boards)
#
#     game_tree = generate_tree()
#
#     return n


# place a move in the global boards
def place(board, num, player):
    global boards
    global curr

    curr = num
    boards[board][num] = player


# read what the server sent us and
# only parses the strings that are necessary
def parse(string, depth=3):
    global curr_board_obj

    if '(' in string:
        command, args = string.split('(')
        args = args.split(')')[0]
        args = args.split(',')
    else:
        command, args = string, []

    if command == 'start':
        if args[0] == 'o':
            curr_board_obj = Board('O')
        else:
            curr_board_obj = Board('X')

    if command == 'second_move':
        curr_board_obj.place(int(args[0]), int(args[1]), 2)
        place(int(args[0]), int(args[1]), 2)
        return play(depth)

    elif command == 'third_move':
        curr_board_obj.place(int(args[1]), int(args[0]), 1)
        curr_board_obj.place(int(args[2]), curr, 2)
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play(depth)

    elif command == 'next_move':
        curr_board_obj.place(int(args[0]), curr, 2)
        place(curr, int(args[0]), 2)
        return play(depth)

    elif command == 'last_move':
        curr_board_obj.place(int(args[0]), curr, 2)
        place(curr, int(args[0]), 2)

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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2])  # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()

        if not text:
            continue

        for line in text.split('\n'):
            response = parse(line)

            if response == -1:
                s.close()
                return

            elif response > 0:
                s.sendall((str(response) + '\n').encode())


if __name__ == '__main__':
    main()
