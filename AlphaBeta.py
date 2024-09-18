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
        actions = [OthelloAction(0,0, True)]
        [max_val, best_action] = self.alpha_beta_algorithm(othello_position, actions, self.search_depth, float('-inf'), float('inf'), othello_position.to_move())
        #print(f"\nmaxinum:  {max_val}, move:")
        #ret.print_move()
        return best_action

    def alpha_beta_algorithm(self, position, action, depth, alpha_value, beta_value, maximizingPlayer):
        #print(f"depth ={depth}"))
        if depth == 0:
            #print(f"\Value:  {self.evaluator.evaluate(position)}, move:")
            #action.print_move()
            position.print_board()
            return (self.evaluator.evaluate(position), action)
        
        if maximizingPlayer:
            #print("White to move")
            max_value = float('-inf')
            list_ = position.get_moves()
            
            a = action
            for item in list_: #each child in the list save the smallest number
                pos = position.make_move(item)
                #item.print_move()
                
                [value, act] = self.alpha_beta_algorithm(pos, item, depth - 1, alpha_value, beta_value, pos.to_move())
                if (alpha_value < value):
                    a = act
                max_value = max(max_value, value)
                alpha_value = max(alpha_value, value)
                if beta_value <= alpha_value:
                    break
            
            #a.print_move()
            return (max_value, a)
        else:
            #print("Black to move")
            max_value = float('inf')
            list_ = position.get_moves()
            
            a = action
            for item in list_: #each child in the list save the smallest number
                pos = position.make_move(item)
                #item.print_move()

                [value, act] = self.alpha_beta_algorithm(pos, item, depth - 1, alpha_value, beta_value, pos.to_move())
                if (beta_value > value):
                    a = act
                max_value = min(max_value, value)
                beta_value = min(beta_value, value)
                if beta_value <= alpha_value:
                    break
            #a.print_move()
            return (max_value, a)
                

        

