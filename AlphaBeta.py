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


    def __init__(self, othello_evaluator=RankedEvaluator(), depth=DefaultDepth):
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
        action = OthelloAction(0,0, True)
        [max_val, ret] = self.alpha_beta_algorithm(othello_position, action, self.DefaultDepth, float('-inf'), float('inf'), othello_position.to_move())
        print(f"maxinum:  {max_val}, move:")
        ret.print_move()
        return ret

    def alpha_beta_algorithm(self, position, action, depth, alpha_value, beta_value, maximizingPlayer):
        if depth == 0:
            return (self.evaluator.evaluate(position), action)
        
        if maximizingPlayer:
            max_value = float('-inf')
            list_ = position.get_moves()
            a = action
            for item in list_: #each child in the list save the smallest number
                pos = position.make_move(item)
                [value, act] = self.alpha_beta_algorithm(pos, item, depth - 1, alpha_value, beta_value, maximizingPlayer)
                if (max_value < value):
                    a = act
                max_value = max(max_value, value)
                alpha_value = max(alpha_value, value)
                if beta_value <= alpha_value:
                    break
            return (max_value, a)
        else:
            min_value = float('inf')
            list_ = position.get_moves()
            a = action
            for item in list_: #each child in the list save the smallest number
                pos = position.make_move(item)
                [value, act] = self.alpha_beta_algorithm(pos, item, depth - 1, alpha_value, beta_value, maximizingPlayer)
                if (max_value > value):
                    a = act
                max_value = min(max_value, value)
                beta_value = min(beta_value, value)
                if beta_value <= alpha_value:
                    break
            return (min_value, a)
                

        

