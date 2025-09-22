import java.util.LinkedList;
import java.util.ListIterator;

/**
 * A simple evaluator that just counts the number of black and white squares
 * 
 * @author Henrik Bj&ouml;rklund
 */
public class RankedEvaluator implements OthelloEvaluator {
	int[][] scoreBoard = {
			{20, -3, 10,  8,  8, 10, -3, 20},
			{-3, -7, -4,  1,  1, -4, -7, -3},
			{10, -4,  2,  3,  3,  2, -4, 10},
			{ 8,  1,  3,  1,  1,  3,  1,  8},
			{ 8,  1,  3,  1,  1,  3,  1,  8},
			{10, -4,  2,  3,  3,  2, -4, 10},
			{-3, -7, -4,  1,  1, -4, -7, -3},
			{20, -3, 10,  8,  8, 10, -3, 20}
	},
	phase1 = {
			{99, -1, 20,  1,  1, 20, -1,  9},
			{-1, -1, -1, -1, -1, -1, -1, -1},
			{20, -1, 20,  3,  3,  9, -1, 20},
			{ 1, -1,  3,  1,  1,  3, -1,  1},
			{ 1, -1,  3,  1,  1,  3, -1,  1},
			{20, -1, 20,  3,  3, 20, -1, 20},
			{-1, -1, -1, -1, -1, -1, -1, -1},
			{ 9, -1, 20,  1,  1, 20, -1, 99}
	},
	phase2 = {
			{99, -9,  9,  3,  3,  9, -9, 99},
			{-9, -9, -1, -1, -1, -1, -9, -9},
			{ 9, -1,  9,  3,  3,  9, -1,  3},
			{ 3, -1,  3,  1,  1,  3, -1,  3},
			{ 3, -1,  3,  1,  1,  3, -1,  3},
			{ 9, -1,  9,  3,  3,  9, -1,  9},
			{-9, -9, -1, -1, -1, -1, -9, -9},
			{99, -9,  9,  3,  3,  9, -9, 99}
	},
	phase3 = {
			{ 9,  1,  1,  1,  1,  1,  1,  9},
			{ 1,  1,  1,  1,  1,  1,  1,  1},
			{ 1,  1,  1,  1,  1,  1,  1,  1},
			{ 1,  1,  1,  1,  1,  1,  1,  1},
			{ 1,  1,  1,  1,  1,  1,  1,  1},
			{ 1,  1,  1,  1,  1,  1,  1,  1},
			{ 1,  1,  1,  1,  1,  1,  1,  1},
			{ 9,  1,  1,  1,  1,  1,  1,  9}
	};



	public int evaluate(OthelloPosition pos) {
		OthelloPosition position = (OthelloPosition) pos;
		int blackSquares = 0;
		int whiteSquares = 0;
		for (int i = 1; i <= OthelloPosition.BOARD_SIZE; i++) {
			for (int j = 1; j <= OthelloPosition.BOARD_SIZE; j++) {
				if (position.board[i][j] == 'W')
					whiteSquares++;
				if (position.board[i][j] == 'B')
					blackSquares++;
			}
		}
		return 	(positionalScore(pos));
	}

	public int countPhase(OthelloPosition pos){
		OthelloPosition position = (OthelloPosition) pos;
		int phase = 0;
		for (int i = 1; i <= OthelloPosition.BOARD_SIZE; i++) {
			for (int j = 1; j <= OthelloPosition.BOARD_SIZE; j++) {
				if (position.board[i][j] != 'E')
					phase++;
			}
		}
		if (phase < 20){
			return 0;
		} else if (phase < 40){
			return 1;
		}
		return -1;
	}

	private int positionalScore(OthelloPosition pos) {
		int score = 0;
		int N = OthelloPosition.BOARD_SIZE;
		char[][] b = pos.board;

		switch (countPhase(pos)) {
			case -1:
				scoreBoard = phase3;
				break;
			case 0:
				scoreBoard = phase1;
				break;
			case 1:
				scoreBoard = phase2;
				break;
		}



		// Loop over the board
		for (int i = 1; i <= N; i++) {
			for (int j = 1; j <= N; j++) {
				int value = scoreBoard[i-1][j-1];

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
		int N = b.length;

		// Top-left corner influence
		if ((i == 0 && j == 1) || (i == 1 && j == 0) || (i == 1 && j == 1)) {
			return b[1][1] != 'E'; // if corner is owned, protection
		}
		// Top-right corner influence
		if ((i == 0 && j == N - 1) || (i == 1 && j == N) || (i == 1 && j == N - 1)) {
			return b[1][N] != 'E';
		}
		// Bottom-left corner influence
		if ((i == N - 1 && j == 0) || (i == N && j == 1) || (i == N - 1 && j == 1)) {
			return b[N][1] != 'E';
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
		int N = OthelloPosition.BOARD_SIZE;

		char[][] b = pos.board;

		// Top-left
		if (b[1][1] == 'W') white++;
		if (b[1][1] == 'B') black++;

		if (b[1][N] == 'W') white++;
		if (b[1][N] == 'B') black++;

		if (b[N][1] == 'W') white++;
		if (b[N][1] == 'B') black++;

		if (b[N][N] == 'W') white++;
		if (b[N][N] == 'B') black++;

		return white - black;
	}

	private int edgesCaptured(OthelloPosition pos) {
		OthelloPosition position = (OthelloPosition) pos;
		int blackSquares = 0;
		int whiteSquares = 0;
		for (int i = 1; i <= OthelloPosition.BOARD_SIZE; i++) {
			if (position.board[i][1] == 'W'
					|| position.board[1][i] == 'W'
					|| position.board[i][OthelloPosition.BOARD_SIZE] == 'W'
					|| position.board[OthelloPosition.BOARD_SIZE][i] == 'W')
				whiteSquares++;
			if (position.board[i][1] == 'B'
					|| position.board[1][i] == 'B'
					|| position.board[i][OthelloPosition.BOARD_SIZE] == 'B'
					|| position.board[OthelloPosition.BOARD_SIZE][i] == 'B')
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
        for (OthelloAction action : moves) {
            flips += position.flipped(action);
        }
		return white ? flips : -flips;
	}

	public void illustrate(OthelloPosition pos) {
		System.out.print("   ");
		for (int i = 1; i <= pos.BOARD_SIZE; i++)
			System.out.print("| " + i + " ");
		System.out.println("|");
		printHorizontalBorder(pos);
		for (int i = 1; i <= pos.BOARD_SIZE; i++) {
			System.out.print(" " + i + " ");
			for (int j = 1; j <= pos.BOARD_SIZE; j++) {
				if (pos.board[i][j] == 'W') {
					System.out.print("| " + scoreBoard[i-1][j-1] + " ");
				} else if (pos.board[i][j] == 'B') {
					System.out.print("|" + (-scoreBoard[i-1][j-1]) + " ");
				} else {
					System.out.print("| " + Math.abs(scoreBoard[i-1][j-1]) + " ");
				}
			}
			System.out.println("| " + i + " ");
			printHorizontalBorder(pos);
		}
		System.out.print("   ");
		for (int i = 1; i <= pos.BOARD_SIZE; i++)
			System.out.print("| " + i + " ");
		System.out.println("|\n");
	}
	private void printHorizontalBorder(OthelloPosition pos) {
		System.out.print("---");
		for (int i = 1; i <= pos.BOARD_SIZE; i++) {
			System.out.print("|---");
		}
		System.out.println("|---");
	}

}
