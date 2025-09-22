import java.util.LinkedList;
import java.util.ListIterator;

/**
 * A simple evaluator that just counts the number of black and white squares
 * 
 * @author Henrik Bj&ouml;rklund
 */
public class RankedEvaluator implements OthelloEvaluator {

	int[][] scoreBoard = {
			{9, -3,  2,  2,  2,  2, -3,  9},
			{-3, -4, -1, -1, -1, -1, -4, -3},
			{ 2, -1,  1,  0,  0,  1, -1,  2},
			{ 2, -1,  0,  1,  1,  0, -1,  2},
			{ 2, -1,  0,  1,  1,  0, -1,  2},
			{ 2, -1,  1,  0,  0,  1, -1,  2},
			{-3, -4, -1, -1, -1, -1, -4, -3},
			{9, -3,  2,  2,  2,  2, -3,  9}
	};

	public int evaluate(OthelloPosition pos) {
		OthelloPosition position = pos.clone();
		LinkedList<OthelloAction> moves = position.getMoves();
		ListIterator<OthelloAction> iterator = moves.listIterator();
		int i = iterator.hasNext() ? 1 : -1;
		return 	i * (positionalScore(pos) + cornersCaptured(pos));
	}

	private int positionalScore(OthelloPosition pos) {
		int score = 0;
		int N = OthelloPosition.BOARD_SIZE - 1;
		char[][] b = pos.board;

		// Loop over the board
		for (int i = 0; i <= N; i++) {
			for (int j = 0; j <= N; j++) {
				int value = scoreBoard[i][j];

				// Adjust for "corner protection":
				// If a corner is captured, its adjacent risky squares lose the penalty
				if (isCornerProtected(b, i, j)) {
					value = Math.abs(value); // make it positive or neutral
				}

				if (b[i][j] == 'W') score += value;
				if (b[i][j] == 'B') score -= value;
			}
		}

		return score;
	}

	private boolean isCornerProtected(char[][] b, int i, int j) {
		int N = b.length - 1;

		// Top-left corner influence
		if ((i == 0 && j == 1) || (i == 1 && j == 0) || (i == 1 && j == 1)) {
			return b[0][0] != 'E'; // if corner is owned, protection
		}
		// Top-right corner influence
		if ((i == 0 && j == N - 1) || (i == 1 && j == N) || (i == 1 && j == N - 1)) {
			return b[0][N] != 'E';
		}
		// Bottom-left corner influence
		if ((i == N - 1 && j == 0) || (i == N && j == 1) || (i == N - 1 && j == 1)) {
			return b[N][0] != 'E';
		}
		// Bottom-right corner influence
		if ((i == N && j == N - 1) || (i == N - 1 && j == N) || (i == N - 1 && j == N - 1)) {
			return b[N][N] != 'E';
		}

		return false;
	}

	private int cornersCaptured(OthelloPosition pos) {
		int white = 0;
		int black = 0;
		int N = OthelloPosition.BOARD_SIZE - 1;

		char[][] b = pos.board;

		// Top-left
		if (b[0][0] == 'W') white++;
		if (b[0][0] == 'B') black++;

		if (b[0][N] == 'W') white++;
		if (b[0][N] == 'B') black++;

		if (b[N][0] == 'W') white++;
		if (b[N][0] == 'B') black++;

		if (b[N][N] == 'W') white++;
		if (b[N][N] == 'B') black++;

		return white - black;
	}

	private int edgesCaptured(OthelloPosition pos) {
		OthelloPosition position = (OthelloPosition) pos;
		int blackSquares = 0;
		int whiteSquares = 0;
		for (int i = 1; i <= OthelloPosition.BOARD_SIZE-1; i++) {
			if (position.board[i][0] == 'W'
					|| position.board[0][i] == 'W'
					|| position.board[i][OthelloPosition.BOARD_SIZE-1] == 'W'
					|| position.board[OthelloPosition.BOARD_SIZE-1][i] == 'W')
				whiteSquares++;
			if (position.board[i][0] == 'B'
					|| position.board[0][i] == 'B'
					|| position.board[i][OthelloPosition.BOARD_SIZE-1] == 'B'
					|| position.board[OthelloPosition.BOARD_SIZE-1][i] == 'B')
				blackSquares++;
		}
		return whiteSquares - blackSquares;
	}

	private int numberOfPossibleFlips(OthelloPosition pos, boolean white) {
		char player = white ? 'W' : 'B';
		int flips = 0;
		OthelloPosition position = pos.clone();
		position.maxPlayer = white;
		LinkedList<OthelloAction> moves = position.getMoves();
		ListIterator<OthelloAction> iterator = moves.listIterator();
		while (iterator.hasNext()) {
			OthelloAction action = iterator.next();
			flips += position.flipped(action);
		}
		return white ? flips : -flips;
	}

}