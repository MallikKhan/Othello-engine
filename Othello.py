from AlphaBeta import AlphaBeta
from OthelloAction import OthelloAction
from RankedEvaluator import RankedEvaluator
from OthelloPosition import OthelloPosition
import argparse
import time

def main(position, time_limit):
    game = OthelloPosition(position)
    if position == "":
        game.initialize()
    start_time = time.time()
    action = OthelloAction(0,0)
    i = 0
    ab_pruning = AlphaBeta(RankedEvaluator())
    while ((time.time() - start_time) < time_limit):
        ab_pruning.set_search_depth(i)
        action = ab_pruning.evaluate(game.clone())
        i += 1
    game.make_move(action)
    action.print_move()


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Process a position and time limit.")
    
    # Add arguments for position and time_limit
    parser.add_argument("position", type=str, help="The position parameter")
    parser.add_argument("time_limit", type=int, help="The time limit in seconds")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args.position, args.time_limit)
