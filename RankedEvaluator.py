from OthelloEvaluator import OthelloEvaluator
from OthelloAction import OthelloAction

class RankedEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        phase = 0


        for y in range(8):
            for x in range(8):
                item = othello_position.board[y][x]  # Board is zero-indexed
                if item == "W" or "B":
                    phase += 1
        
        #Late game
        # Define positional weights matrix (corners, edges, center)
        position_weights = [
            [100, -20,  4,  4,  4,  4, -20, 100],  # row 1 (corners + edges)
            [-20, -50, -1, -1, -1, -1, -50, -20],  # row 2 (adjacent to corners, bad)
            [ 4, -1,  2,  2,  2,  2, -1,  4],  # row 3 (inner squares)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 4 (middle area)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 5 (middle area)
            [ 4, -1,  2,  2,  2,  2, -1,  4],  # row 6 (inner squares)
            [-20, -50, -1, -1, -1, -1, -50, -20],  # row 7 (adjacent to corners, bad)
            [100, -20,  4,  4,  4,  4, -20, 100]   # row 8 (corners + edges)
        ]

        #Early game
        if phase < 16:
            position_weights = [
                [100, -20,  4,  4,  4,  4, -20, 100],  # row 1 (corners + edges)
                [-20, -50, -10, -10, -10, -10, -50, -20],  # row 2 (adjacent to corners, bad)
                [ 4, -10,  20,  10,  10,  20, -10,  4],  # row 3 (inner squares)
                [ 4, -10,  10,  1,  1,  10, -10,  4],  # row 4 (middle area)
                [ 4, -10,  10,  1,  1,  10, -10,  4],  # row 5 (middle area)
                [ 4, -10,  20,  10,  10,  20, -10,  4],  # row 6 (inner squares)
                [-20, -50, -10, -10, -10, -10, -50, -20],  # row 7 (adjacent to corners, bad)
                [100, -20,  4,  4,  4,  4, -20, 100]   # row 8 (corners + edges)
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



    

        if othello_position.to_move():
            all_moves = othello_position.get_moves()
            for item in all_moves:
                x = item.row -1
                y = item.col -1
                white_squares += position_weights[y][x]
        else:
            all_moves = othello_position.get_moves()
            for item in all_moves:
                x = item.row -1
                y = item.col -1
                black_squares += position_weights[y][x]



        return white_squares - black_squares