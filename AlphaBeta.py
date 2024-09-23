from OthelloAlgorithm import OthelloAlgorithm
from CountingEvaluator import CountingEvaluator
from RankedEvaluator import RankedEvaluator
from OthelloAction import OthelloAction


class AlphaBeta(OthelloAlgorithm):
    """
    This is where you implement the alpha-beta algorithm. 
    See OthelloAlgorithm for details

    Author:
    """
    DefaultDepth = 5


    def __init__(self, othello_evaluator=CountingEvaluator(), depth=DefaultDepth):
        self.evaluator = othello_evaluator
        self.search_depth = depth

    def set_evaluator(self, othello_evaluator, ):
        self.evaluator = othello_evaluator  # change to your own evaluator


    def set_search_depth(self, depth):
        self.search_depth = depth  # use iterative deepening search to decide depth


    """
        Returns the OthelloAction the algorithm considers to be the best move given an OthelloPosition
        :param othello_position: The OthelloPosition to evaluate
        :return: The move to make as an OthelloAction
    """
    def evaluate(self, othello_position):
        if othello_position.to_move():
            action = self.maximizing(othello_position, self.search_depth, float('-inf'), float('inf'))
            return action
        else: 
            action = self.minimizing(othello_position, self.search_depth, float('-inf'), float('inf'))
            return action

    def maximizing(self, position, depth, alpha, beta):
        value = float('-inf')
        if depth == 0:
            action = OthelloAction(0, 0)
            action.value = self.evaluator.evaluate(position)
            return action
        
        children = position.get_moves()
        if len(children) == 0:
            pass_move = OthelloAction(0, 0, True)
            pass_position = position.make_move(pass_move)
            pass_move.value = self.evaluator.evaluate(pass_position)
            return pass_move
        
        best_action = OthelloAction(0, 0)
        for child in children:
            child_position = position.make_move(child)
            min_action = self.minimizing(child_position, depth-1, alpha, beta)
            if value < min_action.value:
                child.value = value = min_action.value
                best_action = child

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_action
    
    def minimizing(self, position, depth, alpha, beta):
        value = float('-inf')
        if depth == 0:
            action = OthelloAction(0, 0)
            action.value = self.evaluator.evaluate(position)
            return action
        
        children = position.get_moves()
        if len(children) == 0:
            pass_move = OthelloAction(0, 0, True)
            pass_position = position.make_move(pass_move)
            pass_move.value = self.evaluator.evaluate(pass_position)
            return pass_move
        
        best_action = OthelloAction(0, 0)
        for child in children:
            child_position = position.make_move(child)
            max_action = self.maximizing(child_position, depth-1, alpha, beta)
            if max_action.value < value:
                child.value = value = max_action.value
                best_action = max_action
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_action