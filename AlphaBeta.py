from OthelloAlgorithm import OthelloAlgorithm
from CountingEvaluator import CountingEvaluator
from RankedEvaluator import RankedEvaluator
from OthelloAction import OthelloAction
import time


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

    def set_evaluator(self, othello_evaluator, ):
        self.evaluator = othello_evaluator  # change to your own evaluator


    def set_search_depth(self, depth):
        self.search_depth = depth  # use iterative deepening search to decide depth

    def set_timer(self, time_limit, start_time):
        self.time_limit = time_limit
        self.start_time = start_time


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
        if depth == 0 or ((time.time() - self.start_time) > self.time_limit):
            action = OthelloAction(0, 0)
            action.value = self.evaluator.evaluate(position)
            return action

        if len(moves) == 0:
            pass_move = OthelloAction(0, 0, True)
            pass_move.value = self.evaluator.evaluate(position)
            return pass_move

        best_action = OthelloAction(0, 0)
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


        if depth == 0 or ((time.time() - self.start_time) > self.time_limit):
            action = OthelloAction(0, 0)
            action.value = self.evaluator.evaluate(position)
            return action

        if len(moves) == 0:
            pass_move = OthelloAction(0, 0, True)
            pass_move.value = self.evaluator.evaluate(position)
            return pass_move

        best_action = OthelloAction(0, 0)
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
