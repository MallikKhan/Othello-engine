from OthelloEvaluator import OthelloEvaluator
from OthelloAction import OthelloAction

class RankedEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        position_weights = self.get_pos_weights(othello_position)

        for y in range(8):
            for x in range(8):
                point = position_weights[y][x]
                item = othello_position.board[y][x] 
                if item == 'W':
                    white_squares += point
                elif item == 'B':
                    black_squares += point
        
        if othello_position.to_move():
            white_moves = othello_position.get_moves()
            for move in white_moves:
                x = move.row -1
                y = move.col -1
                white_squares += position_weights[y][x]
        else:
            pos = othello_position.make_move(OthelloAction(0,0, True))
            black_moves = pos.get_moves()
            for move in black_moves:
                x = move.row -1
                y = move.col -1
                black_squares += position_weights[y][x]

        return (white_squares - black_squares)
    
    def get_pos_weights(self, othello_position):
        phase = 0
        for y in range(8):
            for x in range(8):
                if othello_position.board[y][x] != 'E':
                    phase +=1
        
        # Position weights based on board importance
        position_weights = [
            [10, -2,  5,  1,  1,  5, -2, 10],  # row 1 (corners + edges)
            [-2, -5, -5, -5, -5, -5, -5, -2],  # row 2 (adjacent to corners, bad)
            [ 5, -5,  3,  2,  2,  3, -5,  5],  # row 3 (inner squares)
            [ 1, -5,  2,  1,  1,  2, -5,  1],  # row 4 (middle area)
            [ 1, -5,  2,  1,  1,  2, -5,  1],  # row 5 (middle area)
            [ 5, -5,  3,  2,  2,  3, -5,  5],  # row 6 (inner squares)
            [-2, -5, -5, -5, -5, -5, -5, -2],  # row 7 (adjacent to corners, bad)
            [10, -2,  5,  1,  1,  5, -2, 10]   # row 8 (corners + edges)
        ]

        if (phase <= 16):  
            position_weights = [
                [ 10, -10, -10, -10, -10, -10, -10,  10],  # row 1 (corners + edges)
                [-10, -10, -10, -10, -10, -10, -10, -10],  # row 2 (adjacent to corners, bad)
                [-10, -10,  10,   2,   2,  10, -10, -10],  # row 3 (inner squares)
                [-10, -10,   2,   1,   1,   2, -10, -10],  # row 4 (middle area)
                [-10, -10,   2,   1,   1,   2, -10, -10],  # row 5 (middle area)
                [-10, -10,  10,   2,   2,  10, -10, -10],  # row 6 (inner squares)
                [-10, -10, -10, -10, -10, -10, -10, -10],  # row 7 (adjacent to corners, bad)
                [ 10, -10, -10, -10, -10, -10, -10,  10]   # row 8 (corners + edges)
            ]

        

        # Adjust weights based on corner occupation
        # Top-left corner
        if othello_position.board[0][0] != 'E':
            position_weights[1][0] *= -10
            position_weights[0][1] *= -10
            position_weights[1][1] *= -10

        # Top-right corner
        if othello_position.board[0][7] != 'E':
            position_weights[0][6] *= -10
            position_weights[1][6] *= -10
            position_weights[1][7] *= -10

        # Bottom-left corner
        if othello_position.board[7][0] != 'E':
            position_weights[6][0] *= -10
            position_weights[6][1] *= -10
            position_weights[7][1] *= -10

        # Bottom-right corner
        if othello_position.board[7][7] != 'E':
            position_weights[6][6] *= -10
            position_weights[6][7] *= -10
            position_weights[7][6] *= -10

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