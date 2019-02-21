from random import choice
from BoardClasses import Board, Move
from typing import List
import copy
import math
import time
from queue import PriorityQueue
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.


class MoveWithAnalysis(Move):
    def __init__(self, col: int, row: int, heuristic: int) -> None:
        self.heuristic = heuristic
        super().__init__(col, row)

    def __eq__(self, other):
        return self.heuristic == other.heuristic

    def __lt__(self, other):
        return self.heuristic < other.heuristic


class StudentAI():
    col = 0
    row = 0
    k = 0
    g = 0
    moves = 0
    player_number = 2
    opponent_number = 1
    valid_moves = PriorityQueue()
    moves_generated = False

    def __init__(self,col,row,k,g):
        self.g = g
        self.col = col
        self.row = row
        self.k = k
        self.board = Board(col,row,k,g)

    def get_move(self,move):
        start = time.time()
        if move.col == -1 and move.row == -1:
            self.player_number = 1
            self.opponent_number = 2
        else:
            self.board = self.board.make_move(move, self.opponent_number)
            self.moves += 1
        self.moves_generated = False
        my_move = self.iterative_deepening()
        # my_move = self.greedy_search()
        self.board = self.board.make_move(my_move, self.player_number)
        self.moves += 1
        end = time.time()
        # print("Time elapsed: {} seconds".format(end - start))
        return my_move

    # def greedy_search(self) -> Move:
    #     children = self.expand_node(self.board)
    #     best_state = None
    #     for child in children:
    #         result_board = copy.deepcopy(self.board)
    #         result_board.make_move(child)
    #         child.heuristic = self.evaluate_board(result_board, self.player_number)
    #         if best_move is None or child.heuristic > best_move.heuristic:
    #             best_move = child
    #     return best_move

    def iterative_deepening(self) -> MoveWithAnalysis:
        best_state = None
        start_time = time.time()
        for i in range(0, (self.col * self.row) - self.moves):
            state = self.alpha_beta_negamax(self.board, 0, i, -math.inf, math.inf, start_time)
            # print(i)
            if state is not None:
                best_state = state
                # print("Best Move:({}, {}): {}".format(best_state.col, best_state.row, best_state.heuristic))
                # for valid_move in self.valid_moves.queue:
                #     print("({}, {}): {}".format(valid_move.col, valid_move.row, valid_move.heuristic))
                # self.valid_moves.sort(reverse=True)
            else:
                break
        # best_state = self.alpha_beta_negamax(self.board, 0, 1, -math.inf, math.inf, start_time)
        # self.valid_moves.sort(reverse=True)
        # for valid_move in self.valid_moves.queue:
        #     print("({}, {}): {}".format(valid_move.col, valid_move.row, valid_move.heuristic))
        self.valid_moves.queue.clear()
        return best_state

    def alpha_beta_negamax(self, board: Board, depth: int, max_depth: int, alpha: int, beta: int, start_time: int) -> MoveWithAnalysis:
        if time.time() - start_time > 30:
            # print("Depth: {}".format(depth))
            return None
        if board.is_win() or depth > max_depth:
            # print("Depth: {}".format(depth))
            if depth % 2 == 0:
                heuristic = self.evaluate_board(board, self.player_number)
                current_move = MoveWithAnalysis(None, None, heuristic)
                return current_move
            else:
                heuristic = self.evaluate_board(board, self.opponent_number)
                current_move = MoveWithAnalysis(None, None, -heuristic)
                return current_move
        best_move = None
        if self.valid_moves.empty() and not self.moves_generated:
            children = self.expand_node(board)
            for child in children:
                result_board = copy.deepcopy(board)
                result_board = result_board.make_move(child, self.player_number)
                current_move = MoveWithAnalysis(child.col, child.row, 0)
                current_move.heuristic = self.evaluate_board(result_board, self.player_number)
                self.valid_moves.put(current_move)
            self.moves_generated = True
            # self.valid_moves.sort(reverse=True)
        if depth == 0:
            temp_queue = PriorityQueue()
            while not self.valid_moves.empty():
                valid_move = self.valid_moves.get()
                result_board = copy.deepcopy(board)
                result_board = result_board.make_move(valid_move, self.player_number)
                current_move = self.alpha_beta_negamax(result_board, depth + 1, max_depth, -beta, -alpha, start_time)
                if current_move is None:
                    return None
                current_move.col = valid_move.col
                current_move.row = valid_move.row
                current_move.heuristic = -current_move.heuristic
                valid_move.heuristic = current_move.heuristic
                temp_queue.put(valid_move)
                # print("({}, {}): {}".format(valid_move.col, valid_move.row, valid_move.heuristic))
                if best_move is None or current_move.heuristic > best_move.heuristic:
                    best_move = current_move
                if current_move.heuristic > alpha:
                    alpha = current_move.heuristic
                if alpha >= beta:
                    # print("PRUNED")
                    return best_move
            self.valid_moves = temp_queue
        else:
            children = self.expand_node(board)
            for child in children:
                result_board = copy.deepcopy(board)
                if depth % 2 == 0:
                    result_board = result_board.make_move(child, self.player_number)
                else:
                    result_board = result_board.make_move(child, self.opponent_number)
                current_move = self.alpha_beta_negamax(result_board, depth + 1, max_depth, -beta, -alpha, start_time)
                if current_move is None:
                    return None
                current_move.col = child.col
                current_move.row = child.row
                current_move.heuristic = -current_move.heuristic
                if best_move is None or current_move.heuristic > best_move.heuristic:
                    best_move = current_move
                if current_move.heuristic > alpha:
                    alpha = current_move.heuristic
                if alpha >= beta:
                    # print("PRUNED")
                    return best_move
        return best_move
        # children = self.expand_node(board)
        # for child in children:
        #     result_board = copy.deepcopy(board)
        #     if depth % 2 == 0:
        #         result_board = result_board.make_move(child, self.player_number)
        #     else:
        #         result_board = result_board.make_move(child, self.opponent_number)
        #     current_move = self.alpha_beta_negamax(result_board, depth + 1, max_depth, -beta, -alpha, start_time)
        #     if current_move is None:
        #         return None
        #     current_move.col = child.col
        #     current_move.row = child.row
        #     current_move.heuristic = -current_move.heuristic
        #     child.heuristic = current_move.heuristic
        #     if best_move is None or current_move.heuristic > best_move.heuristic:
        #         best_move = current_move
        #     if current_move.heuristic > alpha:
        #         alpha = current_move.heuristic
        #     if alpha >= beta:
        #         # print("PRUNED")
        #         return best_move
        # if depth == 0:
        #     for child in children:
        #         print("({}, {}): {}".format(child.col, child.row, child.heuristic))
        # return best_move

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
                            # print("Evaluated Score: {}".format(math.inf))
                            # board.show_board()
                            return math.inf
                        else:
                            # print("Evaluated Score: {}".format(-math.inf))
                            # board.show_board()
                            return -math.inf
        if tie:
            # print("Evaluated Score: {}".format(1000))
            # board.show_board()
            return 1000
        # print("Evaluated Score: {}".format(score))
        # board.show_board()
        return score

    def expand_node(self, board: Board) -> List:
        children = []
        if self.g == 0:
            for i in range(self.col):
                for j in range(self.row):
                    if board.board[j][i] == 0:
                        children.append(MoveWithAnalysis(i, j, 0))
        else:
            for i in range(self.col):
                if board.board[0][i] == 0:
                    children.append(MoveWithAnalysis(i, 0, 0))
        return children
