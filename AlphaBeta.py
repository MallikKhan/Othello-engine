from OthelloAlgorithm import OthelloAlgorithm
from CountingEvaluator import CountingEvaluator
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
    list_ = othello_position.get_moves()
    value = float('-inf');
    ret = None
    for move in list_:
        temp = alpha_beta_algorithm(move, self.search_depth -1, float('-inf'), float('inf'), othello_position.to_move())
        if (temp > value):
            value = temp
            ret = move
        value = max(temp, value)
    return ret

def alpha_beta_algorithm(self, position, depth, alpha_value, beta_value, maximizingPlayer):
    if depth == 0:
        return self.evaluator(position)
    
    if maximizingPlayer:
        max_value = float('-inf')
        list_ = position.get_moves()
        for item in list_: #each child in the list save the smallest number
            pos = position.make_move(item, item.is_pass_move)
            value = alpha_beta_algorithm(pos, depth - 1, alpha_value, beta_value, maximizingPlayer)
            max_value = max(max_value, value)
            alpha_value = max(alpha_value, value)
            if beta_value <= alpha_value:
                break
        return max_value
    else:
        min_value = float('inf')
        list_ = position.get_moves()
        for item in list_: #each child in the list save the smallest number
            pos = position.make_move(item, item.is_pass_move)
            value = alpha_beta_algorithm(pos, depth - 1, alpha_value, beta_value, maximizingPlayer)
            max_value = min(max_value, value)
            beta_value = min(beta_value, value)
            if beta_value <= alpha_value:
                break
        return min_value
             

    

