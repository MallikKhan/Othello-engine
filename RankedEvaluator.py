from symtable import Class

from OthelloEvaluator import OthelloEvaluator

from OthelloPosition import OthelloPosition
import numpy as np

"""
        This class represents an evaluator that takes a state of the game board
        and uses multiple heuristics to evaluate its value.

        Author: Amer Armoush
"""

class RankedEvaluator(OthelloEvaluator):

    def evaluate(self, othello_position):
        myTiles = oppTiles = myFrontTiles = oppFrontTiles = 0
        discDiff = cornerEval = edgeEval = mobilityEval = stabilityEval = positionalEval = 0
        X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
        stage = self.getGameStage(othello_position)

        # Extract the 8x8 game board (ignoring the borders)
        board = othello_position.board[1:9, 1:9]

        # Define position weights for evaluation
        position_weights = np.array([
            [20, -3, 10,  8,  8, 10, -3, 20],
            [-3, -7, -4,  1,  1, -4, -7, -3],
            [10, -4,  2,  3,  3,  2, -4, 10],
            [ 8,  1,  3,  1,  1,  3,  1,  8],
            [ 8,  1,  3,  1,  1,  3,  1,  8],
            [10, -4,  2,  3,  3,  2, -4, 10],
            [-3, -7, -4,  1,  1, -4, -7, -3],
            [20, -3, 10,  8,  8, 10, -3, 20]
        ])

        # Early game weights if phase is <= 16
        phase = np.count_nonzero(board != "E")
        if phase <= 16:
            position_weights = np.array([
                [10, -3,  2,  2,  2,  2, -3, 10],
                [-3, -5, -1, -1, -1, -1, -5, -3],
                [ 2, -1,  1,  1,  1,  1, -1,  2],
                [ 2, -1,  1,  0,  0,  1, -1,  2],
                [ 2, -1,  1,  0,  0,  1, -1,  2],
                [ 2, -1,  1,  1,  1,  1, -1,  2],
                [-3, -5, -1, -1, -1, -1, -5, -3],
                [10, -3,  2,  2,  2,  2, -3, 10]
            ])

        # Adjust weights based on corner occupation
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for (i, j) in corners:
            if othello_position.board[i + 1][j + 1] != "E":
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if 0 <= i + dx < 8 and 0 <= j + dy < 8:
                            position_weights[i + dx][j + dy] *= -100

        # Calculate score using position weights
        for i in range(othello_position.BOARD_SIZE):
            for j in range(othello_position.BOARD_SIZE):
                if othello_position.is_own_square(i + 1, j + 1):
                    positionalEval += position_weights[i][j]
                    myTiles += 1
                elif othello_position.is_opponent_square(i + 1, j + 1):
                    positionalEval -= position_weights[i][j]
                    oppTiles += 1

                if othello_position.board[i + 1][j + 1] != "E":
                    for k in range(len(X1)):
                        x = i + X1[k]
                        y = j + Y1[k]
                        if 0 <= x < 8 and 0 <= y < 8 and othello_position.board[x + 1][y + 1] == "E":
                            if othello_position.is_own_square(i + 1, j + 1):
                                myFrontTiles += 1
                            else:
                                oppFrontTiles += 1
                            break

<<<<<<< HEAD
        # Disk difference
        if myTiles > oppTiles:
            discDiff = (100.0 * myTiles) / (myTiles + oppTiles)
        elif myTiles < oppTiles:
            discDiff = -(100.0 * oppTiles) / (myTiles + oppTiles)

        # Stability evaluation
        if myFrontTiles > oppFrontTiles:
            stabilityEval = -(100.0 * myFrontTiles) / (myFrontTiles + oppFrontTiles)
        elif myFrontTiles < oppFrontTiles:
            stabilityEval = (100.0 * oppFrontTiles) / (myFrontTiles + oppFrontTiles)

        # Corner and edge evaluations
        cornerEval = self.cornerControl(othello_position)
        edgeEval = self.edgeControl(othello_position)

        # Mobility
        mobilityEval = self.mobilityEval(othello_position)

        # Final weighted score
        score = (10 * discDiff) + (800.0 * cornerEval) + (380.0 * edgeEval) + \
                (80.0 * mobilityEval) + (75.0 * stabilityEval) + (10 * positionalEval)
        return -score

    @staticmethod
    def edgeControl(othello_position):
        myTiles = oppTiles = 0
        positions = [(1, 2), (2, 2), (2, 1), (1, 7), (2, 7), (2, 8), 
                     (8, 2), (7, 2), (7, 8), (8, 7), (7, 7), (8, 8)]
        for pos in positions:
            if othello_position.is_own_square(*pos):
                myTiles += 1
            elif othello_position.is_opponent_square(*pos):
                oppTiles += 1
        return -12.5 * (myTiles - oppTiles)

    @staticmethod
    def mobilityEval(othello_position):
        myMoves = len(othello_position.get_moves())
        othello_position.maxPlayer = not othello_position.maxPlayer
        oppMoves = len(othello_position.get_moves())
        othello_position.maxPlayer = not othello_position.maxPlayer
        if myMoves > oppMoves:
            return (100.0 * myMoves) / (myMoves + oppMoves)
        elif myMoves < oppMoves:
            return -(100.0 * oppMoves) / (myMoves + oppMoves)
        return 0

    @staticmethod
    def getGameStage(othello_position):
        emptyPos = sum(1 for i in range(othello_position.BOARD_SIZE) for j in range(othello_position.BOARD_SIZE) 
                       if othello_position.board[i + 1][j + 1] == "E")
        return 1 if emptyPos >= 30 else 2

    @staticmethod
    def cornerControl(othello_position):
        corners = [(1, 1), (1, 8), (8, 1), (8, 8)]
        myCorners = oppCorners = 0
        for (row, col) in corners:
            if othello_position.is_own_square(row, col):
                myCorners += 1
            elif othello_position.is_opponent_square(row, col):
                oppCorners += 1
        return 25 * (myCorners - oppCorners)
=======
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