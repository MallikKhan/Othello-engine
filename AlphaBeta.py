from OthelloAlgorithm import OthelloAlgorithm
from CountingEvaluator import CountingEvaluator
from RankedEvaluator import RankedEvaluator
from OthelloAction import OthelloAction
import time
from functools import lru_cache


class AlphaBeta(OthelloAlgorithm):
    """
    This is where you implement the alpha-beta algorithm. 
    See OthelloAlgorithm for details

    Author:
    """
    DefaultDepth = 5
    time_limit = 0
    start_time = 0

    def __init__(self, othello_evaluator=CountingEvaluator(), depth=DefaultDepth):
        self.evaluator = othello_evaluator
        self.search_depth = depth
        self.transposition_table = {} 

    def set_evaluator(self, othello_evaluator, ):
        self.evaluator = othello_evaluator  # change to your own evaluator


    def set_search_depth(self, depth):
        self.search_depth = depth  # use iterative deepening search to decide depth

    def set_timer(self, time_limit, start_time):
        self.time_limit = time_limit
        self.start_time = start_time
    
    @lru_cache(maxsize=10000)  # Limit cache size to 10,000 entries
    def transposition_lookup(self, pos_key):
        return self.transposition_table.get(pos_key, None)

    def get_position_key(self, position):
        board_hash = hash(position.board.tostring())  # Fast board hashing
        player_to_move = 1 if position.maxPlayer else 0
        return (board_hash, player_to_move)




    """
        Returns the OthelloAction the algorithm considers to be the best move given an OthelloPosition
        :param othello_position: The OthelloPosition to evaluate
        :return: The move to make as an OthelloAction
    """
    def evaluate(self, othello_position):
        if othello_position.to_move():
            action = self.evaluate_max(othello_position, self.search_depth, float('-inf'), float('inf'))
            return action
        else: 
            action = self.evaluate_min(othello_position, self.search_depth, float('-inf'), float('inf'))
            return action

   
    def evaluate_max(self, position, depth, alpha, beta):
        max_value = float('-inf')
        moves = position.get_moves()

        # Check if the time limit has been reached
        if depth == 0 or len(moves) == 0 or (time.time() - self.start_time) >= self.time_limit:
            action = OthelloAction(0, 0, True)
            action.value = self.evaluator.evaluate(position)
            return action

        best_action = OthelloAction(0, 0, True)
        for move in moves:
            new_position = position.make_move(move)
            min_action = self.evaluate_min(new_position, depth - 1, alpha, beta)
            if max_value < min_action.value:
                move.value = max_value = min_action.value
                best_action = move

            if max_value > alpha:
                alpha = max_value

            if alpha >= beta:
                break

        return best_action


    def evaluate_min(self, position, depth, alpha, beta):
        min_value = float('inf')
        moves = position.get_moves()

        # Check if the time limit has been reached
        if depth == 0 or len(moves) == 0 or (time.time() - self.start_time) >= self.time_limit:
            action = OthelloAction(0, 0, True)
            action.value = self.evaluator.evaluate(position)
            return action

        best_action = OthelloAction(0, 0, True)
        for move in moves:
            new_position = position.make_move(move)
            max_action = self.evaluate_max(new_position, depth - 1, alpha, beta)
            if min_value > max_action.value:
                move.value = min_value = max_action.value
                best_action = move

            if min_value < beta:
                beta = min_value

            if alpha >= beta:
                break

        return best_action

