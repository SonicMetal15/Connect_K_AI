from random import choice
from BoardClasses import Board, Move
from typing import List
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.


class BoardWithAnalysis:
    def __init__(self, board: Board, move: (int, int), heuristic: int) -> None:
        self.board = board
        self.move = move
        self.heuristic = heuristic


class StudentAI():
    col = 0
    row = 0
    k = 0
    g = 0
    player_number = 2

    def __init__(self,col,row,k,g):
        self.g = g
        self.col = col
        self.row = row
        self.k = k
        self.board = Board(col,row,k,g)

    def get_move(self,move):
        if move.col == -1 and move.row == -1:
            self.player_number = 1
        else:
            if self.player_number == 2:
                self.board = self.board.make_move(move, 1)
            else:
                self.board = self.board.make_move(move, 2)
        my_move = self.iterative_deepening(0, self.board, 0, 0, 0)
        self.board = self.board.make_move(my_move, self.player_number)
        return my_move

    def iterative_deepening(self, depth: int, board: Board, turn: int) -> Move:
        valid_moves = self.get_valid_moves(self.board)
        my_move = choice(valid_moves)
        return Move(my_move[0], my_move[1])

    def alpha_beta_minmax(self, depth: int, board: Board, turn: int, alpha: int, beta: int) -> Move:
        return True

    def get_valid_moves(self, board: Board) -> List:
        valid_moves = []
        if self.g == 0:
            for i in range(self.col):
                for j in range(self.row):
                    if board.is_valid_move(i, j):
                        valid_moves.append((i, j))
        else:
            for i in range(self.col):
                if board.board[0][i] == 0:
                    valid_moves.append((i, 0))
        return valid_moves

    def expand_node(self, board: Board, move: (int, int)) -> List:
        return self.get_valid_moves(board)

    def goal_test(self, board: Board) -> int:
        return board.is_win()
