from AlphaBeta import AlphaBeta
from OthelloAction import OthelloAction
from RankedEvaluator import RankedEvaluator
from OthelloPosition import OthelloPosition
import argparse
import time
import sys



def main():
    # Initialize the game position
    game = OthelloPosition()
    game.initialize()
    time_limit = 2
    start_time = time.time()
    best_action = OthelloAction(1, 1, True)  # Initialize the best action
    i = 5  # Start with a search depth of 1
    ab_pruning = AlphaBeta(RankedEvaluator())
    ab_pruning.set_timer(time_limit, start_time)

    # Iterative deepening search
    while (time.time() - start_time) < time_limit or i < 8:
        ab_pruning.set_search_depth(i)
        current_action = ab_pruning.evaluate(game.clone())

        # Update the best action with the result of the current search depth
        if current_action:
            best_action = current_action

        i += 1  # Increase search depth

    # Make the best move after the time limit is reached
    game.make_move(best_action)
    best_action.print_move()
    print(f"Got to depth: {i-1}")
    print(f"Time to search {i-1} depth itteratively: {(time.time() - start_time)}")
    start_time = time.time()
    ab_pruning.set_timer(100, start_time)
    k = 8
    ab_pruning.set_search_depth(k)
    action = ab_pruning.evaluate(game.clone())
    game.make_move(best_action)
    action.print_move()
    print(f"Time to search {k} depth once: {(time.time() - start_time)}")

    Re = RankedEvaluator()
    start_time = time.time()
    Re.evaluate(game.clone())

    print(f"Time to search evaluateboard: {(time.time() - start_time)}")
    start_time = time.time()
    game.make_move(action)
    
    print(f"Time to make move: {(time.time() - start_time)}") 
    



if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        pass
