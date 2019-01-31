from random import choice
from BoardClasses import Board, Move
from typing import List
import copy
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.


class BoardWithAnalysis:
    def __init__(self, board: Board, move: Move, heuristic: int) -> None:
        self.board = board
        self.move = move
        self.heuristic = heuristic


class StudentAI():
    col = 0
    row = 0
    k = 0
    g = 0
    player_number = 2
    opponent_number = 1

    def __init__(self,col,row,k,g):
        self.g = g
        self.col = col
        self.row = row
        self.k = k
        self.board = Board(col,row,k,g)

    def get_move(self,move):
        if move.col == -1 and move.row == -1:
            self.player_number = 1
            self.opponent_number = 2
        else:
            self.board = self.board.make_move(move, self.opponent_number)
        my_move = self.iterative_deepening(0, self.board, 0)
        self.board = self.board.make_move(my_move, self.player_number)
        return my_move

    def iterative_deepening(self, board: Board) -> Move:
        children = self.expand_node(self.board, 0)
        random_state = choice(children)
        return random_state.move

    def alpha_beta_negamax(self, board: Board, limit: int, ply: int) -> Move:
        return True

    def max_value(self, board: Board, alpha: int, beta: int) -> (Move, int):
        return True

    def expand_node(self, board: Board, turn: int) -> List:
        children = []
        if self.g == 0:
            for i in range(self.col):
                for j in range(self.row):
                    if board.is_valid_move(i, j):
                        valid_move = Move(i, j)
                        result_board = copy.deepcopy(board)
                        if turn % 2 == 0:
                            result_board = result_board.make_move(valid_move, self.player_number)
                        else:
                            result_board = result_board.make_move(valid_move, self.opponent_number)
                        children.append(BoardWithAnalysis(result_board, valid_move, 0))
        else:
            for i in range(self.col):
                if board.board[0][i] == 0:
                    valid_move = Move(i, 0)
                    result_board = copy.deepcopy(board)
                    if turn % 2 == 0:
                        result_board = result_board.make_move(valid_move, self.player_number)
                    else:
                        result_board = result_board.make_move(valid_move, self.opponent_number)
                    children.append(BoardWithAnalysis(result_board, valid_move, 0))
        return children

    def goal_test(self, board: Board) -> int:
        return board.is_win()
