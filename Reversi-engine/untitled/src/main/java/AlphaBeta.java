import java.util.LinkedList;
import java.util.ListIterator;

/**
 * This is where you implement the alpha-beta algorithm.
 * See <code>OthelloAlgorithm</code> for details
 *
 * @author Henrik Bj&ouml;rklund
 *
 */
public class AlphaBeta implements OthelloAlgorithm {
	protected int searchDepth;
	protected static final int DefaultDepth = 9;
	protected static final int PosInfty = Integer.MAX_VALUE;
	protected static final int NegInfty = Integer.MIN_VALUE;
	protected OthelloEvaluator evaluator;
	private int timeLimit;
	private long startTime;


	public AlphaBeta() {
		evaluator = new CountingEvaluator();
		searchDepth = DefaultDepth;
	}

	public AlphaBeta(OthelloEvaluator eval) {
		evaluator = eval;
		searchDepth = DefaultDepth;
	}

	public AlphaBeta(OthelloEvaluator eval, int depth) {
		evaluator = eval;
		searchDepth = depth;
	}

	public void setTime(int timeLimit, long startTime){
		this.timeLimit = timeLimit;
		this.startTime = startTime;
	}

	public void setEvaluator(OthelloEvaluator eval) {
		evaluator = eval;
	}

	public void setSearchDepth(int depth) {
		searchDepth = depth;
	}

	public OthelloAction evaluate(OthelloPosition pos) {
		return pos.toMove() ? this.max(pos, this.searchDepth, NegInfty, PosInfty) : this.min(pos, this.searchDepth, NegInfty, PosInfty);
	}

	private OthelloAction max(OthelloPosition position, int depth, int alpha, int beta) {
		int bestValue = NegInfty;
		LinkedList<OthelloAction> moves = position.getMoves();

		// Leaf or terminal node
		if (depth == 0 || moves.isEmpty()) {
			OthelloAction leaf = new OthelloAction(-1, -1, true); // -1,-1 = dummy "evaluation-only"
			leaf.value = evaluator.evaluate(position);
			return leaf;
		}

		OthelloAction bestMove = null;

		for (OthelloAction move : moves) {
			if (System.currentTimeMillis() - startTime >= timeLimit) {
				// Time limit reached → return best so far (or fallback to first move)
				return (bestMove != null) ? bestMove : move;
			}

			OthelloPosition nextPosition = position.makeMove(move);
			OthelloAction reply = min(nextPosition, depth - 1, alpha, beta);

			if (reply.value > bestValue) {
				bestValue = reply.value;
				bestMove = new OthelloAction(move.getRow(), move.getColumn());
				bestMove.value = bestValue;
			}

			alpha = Math.max(alpha, bestValue);
			if (alpha >= beta) {
				break; // Beta cutoff
			}
		}

		return bestMove;
	}

	private OthelloAction min(OthelloPosition position, int depth, int alpha, int beta) {
		int bestValue = PosInfty;
		LinkedList<OthelloAction> moves = position.getMoves();

		// Leaf or terminal node
		if (depth == 0 || moves.isEmpty()) {
			OthelloAction leaf = new OthelloAction(-1, -1, true);
			leaf.value = evaluator.evaluate(position);
			return leaf;
		}

		OthelloAction bestMove = null;

		for (OthelloAction move : moves) {
			if (System.currentTimeMillis() - startTime >= timeLimit) {
				// Time limit reached → return best so far (or fallback to first move)
				return (bestMove != null) ? bestMove : move;
			}

			OthelloPosition nextPosition = position.makeMove(move);
			OthelloAction reply = max(nextPosition, depth - 1, alpha, beta);

			if (reply.value < bestValue) {
				bestValue = reply.value;
				bestMove = new OthelloAction(move.getRow(), move.getColumn());
				bestMove.value = bestValue;
			}

			beta = Math.min(beta, bestValue);
			if (beta <= alpha) {
				break; // Alpha cutoff
			}
		}

		return bestMove;
	}

}