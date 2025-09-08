from OthelloEvaluator import OthelloEvaluator
from OthelloAction import OthelloAction
import numpy as np

class RankedEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        # Extract the 8x8 game board (ignoring the borders)
        board = othello_position.board[1:9, 1:9]

        # Define position weights for evaluation
        position_weights = np.array([
            [20, -3, 10,  8,  8, 10, -3, 20],   # Corners remain highly valuable
            [-3, -7, -4,  1,  1, -4, -7, -3],   # Edges near corners are still dangerous
            [10, -4,  2,  3,  3,  2, -4, 10],   # Inner squares become more valuable
            [ 8,  1,  3,  1,  1,  3,  1,  8],   # Middle area slightly less valuable
            [ 8,  1,  3,  1,  1,  3,  1,  8],   # Middle area slightly less valuable
            [10, -4,  2,  3,  3,  2, -4, 10],   # Inner squares become more valuable
            [-3, -7, -4,  1,  1, -4, -7, -3],   # Edges near corners are still dangerous
            [20, -3, 10,  8,  8, 10, -3, 20]    # Corners remain highly valuable
        ])

        # Early game weights if phase is <= 16
        phase = np.count_nonzero(board != 'E')
        if phase <= 16:
            position_weights = np.array([
                [10, -3,  2,  2,  2,  2, -3, 10],  # Corners are highly valuable, adjacent to corners is bad
                [-3, -5, -1, -1, -1, -1, -5, -3],  # Positions next to corners are dangerous
                [ 2, -1,  1,  1,  1,  1, -1,  2],  # Inner positions provide moderate stability
                [ 2, -1,  1,  0,  0,  1, -1,  2],  # Middle areas are neutral
                [ 2, -1,  1,  0,  0,  1, -1,  2],  # Middle areas are neutral
                [ 2, -1,  1,  1,  1,  1, -1,  2],  # Inner positions provide moderate stability
                [-3, -5, -1, -1, -1, -1, -5, -3],  # Avoid positions next to corners
                [10, -3,  2,  2,  2,  2, -3, 10]   # Corners are highly valuable
            ])

        # Adjust weights based on corner occupation
        if othello_position.board[0][0] != 'E':  # Top-left corner
            position_weights[1][0] *= -100
            position_weights[0][1] *= -100
            position_weights[1][1] *= -100
        if othello_position.board[0][7] != 'E':  # Top-right corner
            position_weights[0][6] *= -100
            position_weights[1][6] *= -100
            position_weights[1][7] *= -100
        if othello_position.board[7][0] != 'E':  # Bottom-left corner
            position_weights[6][0] *= -100
            position_weights[6][1] *= -100
            position_weights[7][1] *= -100
        if othello_position.board[7][7] != 'E':  # Bottom-right corner
            position_weights[6][6] *= -100
            position_weights[6][7] *= -100
            position_weights[7][6] *= -100

        # Calculate score using position weights
        white_score = np.sum(position_weights[board == 'W'])
        black_score = np.sum(position_weights[board == 'B'])

        # Use raw stone counts for additional evaluation (optional)
        white_squares = np.sum(board == 'W')
        black_squares = np.sum(board == 'B')

        # You can weigh raw counts more or less depending on your evaluation strategy
        return (white_score - black_score) + (white_squares - black_squares)
    
    def get_pos_weights(self, othello_position):
        phase = 0
        board = othello_position.board
        for y in range(8):
            for x in range(8):
                if board[y][x] != 'E':
                    phase +=1
        
        # Position weights based on board importance
        position_weights = [
            [10, -2,  4,  4,  4,  4, -2, 10],  # row 1 (corners + edges)
            [-2, -5, -1, -1, -1, -1, -5, -2],  # row 2 (adjacent to corners, bad)
            [ 4, -1,  3,  2,  2,  3, -1,  4],  # row 3 (inner squares)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 4 (middle area)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 5 (middle area)
            [ 4, -1,  3,  2,  2,  3, -1,  4],  # row 6 (inner squares)
            [-2, -5, -1, -1, -1, -1, -5, -2],  # row 7 (adjacent to corners, bad)
            [10, -2,  4,  4,  4,  4, -2, 10]   # row 8 (corners + edges)
        ]
        
        # Adjust weights based on corner occupation
        # Top-left corner
        if board[0][0] != 'E':
            position_weights[1][0] = 100
            position_weights[0][1] = 100
            position_weights[1][1] = 100

        # Top-right corner
        if board[0][7] != 'E':
            position_weights[0][6] = 100
            position_weights[1][6] = 100
            position_weights[1][7] = 100

        # Bottom-left corner
        if board[7][0] != 'E':
            position_weights[6][0] = 100
            position_weights[6][1] = 100
            position_weights[7][1] = 100

        # Bottom-right corner
        if board[7][7] != 'E':
            position_weights[6][6] = 100
            position_weights[6][7] = 100
            position_weights[7][6] = 100

        return position_weights
    
    def mobility(self, othello_position):
        white = 0
        black = 0
        if othello_position.to_move():
            white = len(othello_position.get_moves())
            pos = othello_position.make_move(OthelloAction(0,0, True))
            black = len(pos.get_moves())
        else:
            black = len(othello_position.get_moves())
            pos = othello_position.make_move(OthelloAction(0,0, True))
            white = len(pos.get_moves())
        return white - black