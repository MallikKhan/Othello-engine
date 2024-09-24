from OthelloEvaluator import OthelloEvaluator
from OthelloAction import OthelloAction

class RankedEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        
        # Position weights based on board importance
        position_weights = [
            [100, -20,  4,  4,  4,  4, -20, 100],  # row 1 (corners + edges)
            [-20, -50, -1, -1, -1, -1, -50, -20],  # row 2 (adjacent to corners, bad)
            [ 4, -1,  2,  2,  2,  2, -1,  4],  # row 3 (inner squares)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 4 (middle area)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 5 (middle area)
            [ 4, -1,  2,  2,  2,  2, -1,  4],  # row 6 (inner squares)
            [-2, -5, -1, -1, -1, -1, -5, -2],  # row 7 (adjacent to corners, bad)
            [10, -2,  4,  4,  4,  4, -2, 10]   # row 8 (corners + edges)
        ]
        

        # Adjust weights based on corner occupation
        # Top-left corner
        if othello_position.board[0][0] != 'E':
            position_weights[1][0] *= -100
            position_weights[0][1] *= -100
            position_weights[1][1] *= -100


        # Top-right corner
        if othello_position.board[0][7] != 'E':
            position_weights[0][6] *= -100
            position_weights[1][6] *= -100
            position_weights[1][7] *= -100

        # Bottom-left corner
        if othello_position.board[7][0] != 'E':
            position_weights[6][0] *= -100
            position_weights[6][1] *= -100
            position_weights[7][1] *= -100

        # Bottom-right corner
        if othello_position.board[7][7] != 'E':
            position_weights[6][6] *= -100
            position_weights[6][7] *= -100
            position_weights[7][6] *= -100

        # Calculating score
        for y in range(8):
            for x in range(8):
                point = position_weights[y][x]
                item = othello_position.board[y][x]  # Board is zero-indexed
                
                if item == 'W':
                    white_squares += point
                elif item == 'B':
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

""" 
class RankedEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        phase = 0
        for y in range(8):
            for x in range(8):
                item = othello_position.board[y][x]  # Board is zero-indexed
                if item == 'W' or item  == 'B':
                    phase  += 1

        
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

        return heuristic_value
 """

