from AlphaBeta import AlphaBeta
from OthelloAction import OthelloAction
from RankedEvaluator import RankedEvaluator
from OthelloPosition import OthelloPosition
import argparse
import time
import sys

# Function to validate the position string
def validate_position_string(position):
    if len(position) != 65:
        if len(position) > 65:
            sys.stderr.write("Error: Position string is too long. Expected 65 characters.\n")
        else:
            sys.stderr.write("Error: Position string is too short. Expected 65 characters.\n")
        sys.exit(1)

def main(position, time_limit):
    # Validate the position string
    validate_position_string(position)

    # Initialize the game position
    game = OthelloPosition(position)
    if position == "":
        game.initialize()

    start_time = time.time()
    best_action = OthelloAction(1, 1)  # Initialize the best action
    i = 1  # Start with a search depth of 1
    ab_pruning = AlphaBeta(RankedEvaluator())
    ab_pruning.set_timer(time_limit, start_time)

    # Iterative deepening search
    while (time.time() - start_time) < time_limit:
        ab_pruning.set_search_depth(i)
        current_action = ab_pruning.evaluate(game.clone())

        # Update the best action with the result of the current search depth
        if current_action:
            best_action = current_action

        i += 1  # Increase search depth

    # Make the best move after the time limit is reached
    game.make_move(best_action)
    best_action.print_move()


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Process a position and time limit.")
    
    # Add arguments for position and time_limit
    parser.add_argument("position", type=str, help="The position parameter")
    parser.add_argument("time_limit", type=int, help="The time limit in seconds")

    try:
        # Parse the arguments
        args = parser.parse_args()

        # Validate that time_limit is positive
        if args.time_limit <= 0:
            sys.stderr.write("Error: Time limit must be a positive integer.\n")
            sys.exit(1)

        # Call the main function with the parsed arguments
        main(args.position, args.time_limit)

    except argparse.ArgumentError as e:
        sys.stderr.write(f"Argument error: {e}\n")
        sys.exit(1)

    except SystemExit as e:
        # argparse already handles the error, no need to reprint
        pass
