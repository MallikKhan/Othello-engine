from OthelloEvaluator import OthelloEvaluator

class RankedEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        
        # Position weights based on board importance
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
        for y in range(8):
            for x in range(8):
                point = position_weights[y][x]
                item = othello_position.board[y][x]  # Board is zero-indexed
                
                if item == "W":
                    white_squares += point
                elif item == "B":
                    black_squares += point

        # The heuristic returns the difference in scores (favoring the current player)
        return white_squares - black_squares