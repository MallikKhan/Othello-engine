from OthelloEvaluator import OthelloEvaluator
from OthelloAction import OthelloAction

class RankedEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        
        # Define positional weights matrix (corners, edges, center)
        position_weights = [
            [10, -2,  4,  4,  4,  4, -2, 10],  # row 1 (corners + edges)
            [-2, -5, -1, -1, -1, -1, -5, -2],  # row 2 (adjacent to corners, bad)
            [ 4, -1,  2,  2,  2,  2, -1,  4],  # row 3 (inner squares)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 4 (middle area)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 5 (middle area)
            [ 4, -1,  2,  2,  2,  2, -1,  4],  # row 6 (inner squares)
            [-2, -5, -1, -1, -1, -1, -5, -2],  # row 7 (adjacent to corners, bad)
            [10, -2,  4,  4,  4,  4, -2, 10]   # row 8 (corners + edges)
        ]
        
        # Count discs for each player and evaluate positional value
        for y in range(8):
            for x in range(8):
                point = position_weights[y][x]
                item = othello_position.board[y][x]  # Board is zero-indexed
                
                if item == "W":
                    white_squares += point
                elif item == "B":
                    black_squares += point

        # Calculate mobility for both players
        white_mobility = len(othello_position.get_moves())
        black_mobility = len(othello_position.get_moves())
        if (othello_position.to_move()):
            pos = othello_position.make_move(OthelloAction(0, 0, True))
            black_mobility = len(pos.get_moves())
        else: 
            pos = othello_position.make_move(OthelloAction(0, 0, True))
            white_mobility = len(pos.get_moves())


        # Frontier discs: count how many discs are adjacent to empty squares
        white_frontier = self.count_frontier_discs(othello_position, "W")
        black_frontier = self.count_frontier_discs(othello_position, "B")

        # Stability: count stable discs (discs that cannot be flipped)
        white_stability = self.count_stable_discs(othello_position, "W")
        black_stability = self.count_stable_discs(othello_position, "B")

        # Combine the factors into the final heuristic value
        positional_value = white_squares - black_squares
        mobility_value = white_mobility - black_mobility
        frontier_value = black_frontier - white_frontier  # Fewer frontier discs is better
        stability_value = white_stability - black_stability

        # Weighting the factors (you can tune these weights based on experimentation)
        weight_positional = 10
        weight_mobility = 5
        weight_frontier = 3
        weight_stability = 8

        heuristic_value = (
            weight_positional * positional_value +
            weight_mobility * mobility_value +
            weight_frontier * frontier_value +
            weight_stability * stability_value
        )

        return heuristic_value

    def count_frontier_discs(self, othello_position, player):
        # Count the number of frontier discs for the given player
        frontier_count = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for y in range(8):
            for x in range(8):
                if othello_position.board[y][x] == player:
                    for dy, dx in directions:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < 8 and 0 <= nx < 8 and othello_position.board[ny][nx] == ".":
                            frontier_count += 1
                            break
        return frontier_count

    def count_stable_discs(self, othello_position, player):
        # A simple method to count stable discs (discs that cannot be flipped)
        stable_count = 0
        # Simple check for corners (advanced stable-disc detection would be more complex)
        stable_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]  # Corners
        for y, x in stable_positions:
            if othello_position.board[y][x] == player:
                stable_count += 1
        # Advanced stable-disc detection can be added here based on edge-stability algorithms
        return stable_count
