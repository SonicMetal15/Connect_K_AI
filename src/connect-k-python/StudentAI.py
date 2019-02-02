from random import choice
from BoardClasses import Board, Move
from typing import List
import copy
import math
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
        # my_move = self.iterative_deepening(self.board)
        my_move = self.greedy_search()
        self.board = self.board.make_move(my_move, self.player_number)
        return my_move

    def greedy_search(self) -> Move:
        children = self.expand_node(self.board, 0)
        best_state = None
        for state in children:
            if state.heuristic > best_state.heuristic:
                best_state = state
        return best_state.move

    def iterative_deepening(self) -> Move:
        for i in range(0, math.inf):
            my_move = self.alpha_beta_negamax(i)
        return my_move

    def alpha_beta_negamax(self, limit: int) -> Move:
        alpha = -math.inf
        beta = math.inf
        my_move = None
        children = self.expand_node(self.board, 0)
        for child in children:

        return True

    # def max_value(self, board: Board, alpha: int, beta: int) -> (Move, int):
    #     return True

    def evaluate_board(self, board: Board, player_evaluated: int) -> int:
        score = 0
        steps = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        tie = True
        for i in range(self.row):
            for j in range(self.col):
                if board.board[i][j] == 0:
                    tie = False
                    continue
                first_player = board.board[i][j]
                for step in steps:
                    is_win = True
                    temp_row = i
                    temp_col = j
                    temp_score = 0
                    for pieces in range(1, self.k):
                        temp_row += step[0]
                        temp_col += step[1]
                        if not board.is_valid_move(temp_col, temp_row, False):
                            is_win = False
                            if pieces < self.k:
                                temp_score = 0
                            break
                        if board.board[temp_row][temp_col] != first_player and board.board[temp_row][temp_col] != 0:
                            is_win = False
                            temp_score = 0
                            break
                        elif board.board[temp_row][temp_col] == 0:
                            is_win = False
                            temp_score += 1
                        else:
                            temp_score += (pieces * 2)
                    if player_evaluated == first_player:
                        score += (temp_score + 1)
                    else:
                        score -= (temp_score + 1)
                    if is_win:
                        if first_player == self.player_number:
                            print("Evaluated Score: {}".format(math.inf))
                            board.show_board()
                            return math.inf
                        else:
                            print("Evaluated Score: {}".format(-math.inf))
                            board.show_board()
                            return -math.inf
        if tie:
            print("Evaluated Score: {}".format(1000))
            board.show_board()
            return 1000
        print("Evaluated Score: {}".format(score))
        board.show_board()
        return score

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
                            heuristic = self.evaluate_board(result_board, self.player_number)
                        else:
                            result_board = result_board.make_move(valid_move, self.opponent_number)
                            heuristic = self.evaluate_board(result_board, self.opponent_number)
                        children.append(BoardWithAnalysis(result_board, valid_move, heuristic))
        else:
            for i in range(self.col):
                if board.board[0][i] == 0:
                    valid_move = Move(i, 0)
                    result_board = copy.deepcopy(board)
                    if turn % 2 == 0:
                        result_board = result_board.make_move(valid_move, self.player_number)
                        heuristic = self.evaluate_board(result_board, self.player_number)
                    else:
                        result_board = result_board.make_move(valid_move, self.opponent_number)
                        heuristic = self.evaluate_board(result_board, self.opponent_number)
                    children.append(BoardWithAnalysis(result_board, valid_move, heuristic))
        return children
