import numpy as np
from OthelloAction import OthelloAction


class OthelloPosition(object):
    """
    This class is used to represent game positions. It uses a 2-dimensional char array for the board
    and a Boolean to keep track of which player has the move.

    For convenience, the array actually has two columns and two rows more that the actual game board.
    The 'middle' is used for the board. The first index is for rows, and the second for columns.
    This means that for a standard 8x8 game board, board[1][1] represents the upper left corner,
    board[1][8] the upper right corner, board[8][1] the lower left corner, and board[8][8] the lower left corner.

    Author: Ola Ringdahl
    """

    def __init__(self, board_str=""):
        """
        Creates a new position according to str. If str is not given all squares are set to E (empty)
        :param board_str: A string of length 65 representing the board. The first character is W or B, indicating which
        player is to move. The remaining characters should be E (for empty), O (for white markers), or X (for black
        markers).
        """
        self.BOARD_SIZE = 8
        self.maxPlayer = True
        self.board = np.array([['E' for col in range(self.BOARD_SIZE + 2)] for row in range(self.BOARD_SIZE + 2)])
        if len(list(board_str)) >= 65:
            if board_str[0] == 'W':
                self.maxPlayer = True
            else:
                self.maxPlayer = False
            for i in range(1, len(list(board_str))):
                col = ((i - 1) % 8) + 1
                row = (i - 1) // 8 + 1
                # For convenience we use W and B in the board instead of X and O:
                if board_str[i] == 'X':
                    self.board[row][col] = 'B'
                elif board_str[i] == 'O':
                    self.board[row][col] = 'W'

    def initialize(self):
        """
        Initializes the position by placing four markers in the middle of the board.
        :return: Nothing
        """
        self.board[self.BOARD_SIZE // 2][self.BOARD_SIZE // 2] = 'W'
        self.board[self.BOARD_SIZE // 2 + 1][self.BOARD_SIZE // 2 + 1] = 'W'
        self.board[self.BOARD_SIZE // 2][self.BOARD_SIZE // 2 + 1] = 'B'
        self.board[self.BOARD_SIZE // 2 + 1][self.BOARD_SIZE // 2] = 'B'
        self.maxPlayer = True

    def make_move(self, action):
        """
        Perform the move suggested by the OhelloAction action and return the new position. Observe that this also
        changes the player to move next.
        :param action: The move to make as an OthelloAction
        :return: The OthelloPosition resulting from making the move action in the current position.
        """
        # TODO: write the code for this method and whatever helper methods it need
        ret = self.clone()
        if action.is_pass_move:
            ret.maxPlayer = not self.maxPlayer
        elif self.maxPlayer:
            ret.board[action.row][action.col] = 'W'
            ret.maxPlayer = False
            ret.flip_stones(action, 'W')
        else:
            ret.board[action.row][action.col] = 'B'
            ret.maxPlayer = True
            ret.flip_stones(action, 'B')

        return ret
    
    def flip(self, action):
        if self.board[action.row][action.col] == 'W':
            self.board[action.row][action.col] = 'B'
        else:
            self.board[action.row][action.col] = 'W'


    def flip_stones(self, action, player):
        opponent = 'W' if player == 'B' else 'B'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Up, Down, Left, Right
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonals

        for direction in directions:
            row, col = action.row + direction[0], action.col + direction[1]
            stones_to_flip = []

            while self.is_inbound(row, col) and self.board[row][col] == opponent:
                stones_to_flip.append(OthelloAction(row, col))
                row += direction[0]
                col += direction[1]

            # If we find a player's own stone after opponent's stones, we can flip them
            if self.is_inbound(row, col) and self.board[row][col] == player:
                if len(stones_to_flip) > 0:
                    for a in stones_to_flip:
                        self.flip(a)
        
    
    def is_inbound(self, row, col):
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE


    def get_moves(self):
        """
        Get all possible moves for the current position, sorted by the desirability
        of the move (e.g., corners are favored, edges less so, etc.).
        :return: A list of OthelloAction representing all possible moves in the position,
        sorted with favored moves first.
        """
        moves = []
        favored_positions = [
            [10, -2,  4,  4,  4,  4, -2, 10],  # row 1 (corners + edges)
            [-2, -5, -1, -1, -1, -1, -5, -2],  # row 2 (adjacent to corners, bad)
            [ 4, -1,  3,  2,  2,  3, -1,  4],  # row 3 (inner squares)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 4 (middle area)
            [ 4, -1,  2,  1,  1,  2, -1,  4],  # row 5 (middle area)
            [ 4, -1,  3,  2,  2,  3, -1,  4],  # row 6 (inner squares)
            [-2, -5, -1, -1, -1, -1, -5, -2],  # row 7 (adjacent to corners, bad)
            [10, -2,  4,  4,  4,  4, -2, 10]   # row 8 (corners + edges)
        ]

        append = moves.append
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.__is_candidate(i + 1, j + 1) and self.__is_move(i + 1, j + 1):
                    # Calculate the score of the move based on its board position
                    score = favored_positions[i][j]
                    append((score, OthelloAction(i + 1, j + 1)))

        # Sort moves by score, with highest (favored) moves appearing first
        moves.sort(reverse=True, key=lambda x: x[0])

        # Return only the list of actions, not the scores
        return [move for score, move in moves]


    def __is_candidate(self, row, col):
        """
        Check if a position is a candidate for a move (empty and has a neighbour)
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is a candidate
        """
        if self.board[row][col] != 'E':
            return False
        if self.__has_neighbour(row, col):
            return True
        return False

    def __is_move(self, row, col):
        """
        Check if it is possible to do a move from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if row < 1 or row > self.BOARD_SIZE or col < 1 or col > self.BOARD_SIZE:
            return False
        if self.__check_north(row, col):
            return True
        if self.__check_north_east(row, col):
            return True
        if self.__check_east(row, col):
            return True
        if self.__check_south_east(row, col):
            return True
        if self.__check_south(row, col):
            return True
        if self.__check_south_west(row, col):
            return True
        if self.__check_west(row, col):
            return True
        if self.__check_north_west(row, col):
            return True

    def __check_north(self, row, col):
        """
        Check if it is possible to do a move to the north from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row - 1, col):
            return False
        i = row - 2
        while i > 0:
            if self.board[i][col] == 'E':
                return False
            if self.__is_own_square(i, col):
                return True
            i -= 1
        return False

    def __check_north_east(self, row, col):
        """
        Check if it is possible to do a move to the north east from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row - 1, col + 1):
            return False
        i = 2
        while row - i > 0 and col + i <= self.BOARD_SIZE:
            if self.board[row - i][col + i] == 'E':
                return False
            if self.__is_own_square(row - i, col + i):
                return True
            i += 1
        return False

    def __check_north_west(self, row, col):
        """
        Check if it is possible to do a move to the north west from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row - 1, col - 1):
            return False
        i = 2
        while row - i > 0 and col - i > 0:
            if self.board[row - i][col - i] == 'E':
                return False
            if self.__is_own_square(row - i, col - i):
                return True
            i += 1
        return False

    def __check_south(self, row, col):
        """
        Check if it is possible to do a move to the south from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row + 1, col):
            return False
        i = row + 2
        while i <= self.BOARD_SIZE:
            if self.board[i][col] == 'E':
                return False
            if self.__is_own_square(i, col):
                return True
            i += 1
        return False

    def __check_south_east(self, row, col):
        """
        Check if it is possible to do a move to the south east from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row + 1, col + 1):
            return False
        i = 2
        while row + i <= self.BOARD_SIZE and col + i <= self.BOARD_SIZE:
            if self.board[row + i][col + i] == 'E':
                return False
            if self.__is_own_square(row + i, col + i):
                return True
            i += 1
        return False

    def __check_south_west(self, row, col):
        """
        Check if it is possible to do a move to the south west from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row + 1, col - 1):
            return False
        i = 2
        while row + i <= self.BOARD_SIZE and col - i > 0:
            if self.board[row + i][col - i] == 'E':
                return False
            if self.__is_own_square(row + i, col - i):
                return True
            i += 1
        return False

    def __check_west(self, row, col):
        """
        Check if it is possible to do a move to the west from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row, col - 1):
            return False
        i = col - 2
        while i > 0:
            if self.board[row][i] == 'E':
                return False
            if self.__is_own_square(row, i):
                return True
            i -= 1
        return False

    def __check_east(self, row, col):
        """
        Check if it is possible to do a move to the east from this position
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it is possible to do a move
        """
        if not self.__is_opponent_square(row, col + 1):
            return False
        i = col + 2
        while i <= self.BOARD_SIZE:
            if self.board[row][i] == 'E':
                return False
            if self.__is_own_square(row, i):
                return True
            i += 1
        return False

    def __is_opponent_square(self, row, col):
        """
        Check if the position is occupied by the opponent
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if opponent square
        """
        if self.maxPlayer and self.board[row][col] == 'B':
            return True
        if not self.maxPlayer and self.board[row][col] == 'W':
            return True
        return False

    def __is_own_square(self, row, col):
        """
        Check if the position is occupied by the player
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if it's your own square
        """
        if not self.maxPlayer and self.board[row][col] == 'B':
            return True
        if self.maxPlayer and self.board[row][col] == 'W':
            return True
        return False

    def __has_neighbour(self, row, col):
        """
        Check if the position has any non-empty squares
        :param row: The row of the board position
        :param col: The column of the board position
        :return: True if has neighbours
        """
        if self.board[row - 1][col] != 'E':
            return True
        if self.board[row - 1, col + 1] != 'E':
            return True
        if self.board[row - 1][col - 1] != 'E':
            return True
        if self.board[row][col - 1] != 'E':
            return True
        if self.board[row][col + 1] != 'E':
            return True
        if self.board[row + 1][col - 1] != 'E':
            return True
        if self.board[row + 1][col + 1] != 'E':
            return True
        if self.board[row + 1][col] != 'E':
            return True
        return False

    def to_move(self):
        """
        Check which player's turn it is
        :return: True if the first player (white) has the move, otherwise False
        """
        return self.maxPlayer

    def clone(self):
        """
        Copy the current position
        :return: A new OthelloPosition, identical to the current one.
        """
        ot = OthelloPosition("")
        ot.board = np.copy(self.board)
        ot.maxPlayer = self.maxPlayer
        return ot

    def print_board(self):
        """
        Prints the current board with column and row labels in the desired format.
        :return: Nothing
        """
        # Column headers
        print("   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")
        print("---|---|---|---|---|---|---|---|---|---")

        for row_idx, row in enumerate(self.board, start=-1):
            # Row number before the cells
            print(f" {row_idx} |", end="")
            for item in row:
                if item == 'E':
                    print("   |", end="")
                elif item == 'B':
                    print(" X |", end="")
                else:
                    print(" O |", end="")
            # Row number after the cells
            print(f" {row_idx}")
            print("---|---|---|---|---|---|---|---|---|---")

        # Column headers at the bottom
        print("   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")

        # print("ToMove: ", self.maxPlayer)
