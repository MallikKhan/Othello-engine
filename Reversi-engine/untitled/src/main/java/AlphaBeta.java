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

	private OthelloAction max(OthelloPosition position, int depth, int alpha, int beta){
		int minValue = NegInfty;
		LinkedList<OthelloAction> moves = position.getMoves();
		ListIterator<OthelloAction> movesIterator = moves.listIterator();
		OthelloAction move;

		if (depth == 0) {
			move = new OthelloAction(0, 0);
			move.value = this.evaluator.evaluate(position);
		} else if (!movesIterator.hasNext()) {
			move = new OthelloAction(0, 0, true);
			move.value = this.evaluator.evaluate(position);
		} else {
			OthelloAction maximizingMove = new OthelloAction(0, 0);

			
			while (movesIterator.hasNext()){
				move = movesIterator.next();
				OthelloPosition nextPosition = position.makeMove(move);
				OthelloAction minimizingMove = this.min(nextPosition, depth-1, alpha, beta);
				
				if (minValue < minimizingMove.value) {
					move.value = minValue = minimizingMove.value;
					maximizingMove = move;
				}
				
				if (minValue >= beta) {
					move.value = minValue;
					return move;
				}
				
				if (minValue > alpha){
					alpha = minValue;
				}
			}
			
			return maximizingMove;
		}
		return move;
	}

	private OthelloAction min(OthelloPosition position, int depth, int alpha, int beta){
		int maxValue = PosInfty;
		LinkedList<OthelloAction> moves = position.getMoves();
		ListIterator<OthelloAction> movesIterator = moves.listIterator();
		OthelloAction move;
		if (depth == 0) {
			move = new OthelloAction(0, 0);
			move.value = this.evaluator.evaluate(position);
		} else if (!movesIterator.hasNext()) {
			move = new OthelloAction(0, 0, true);
			move.value = this.evaluator.evaluate(position);
		} else {
			OthelloAction minimizingMove = new OthelloAction(0, 0);
			moves = position.getMoves();
			movesIterator = moves.listIterator();

			while (movesIterator.hasNext() && System.currentTimeMillis() - startTime < timeLimit){
				move = movesIterator.next();
				OthelloPosition nextPosition = position.makeMove(move);
				OthelloAction maximizingMove = this.max(nextPosition, depth-1, alpha, beta);

				if (maxValue > maximizingMove.value) {
					move.value = maxValue = maximizingMove.value;
					minimizingMove = move;
				}

				if (maxValue <= alpha) {
					move.value = maxValue;
					return move;
				}

				if (maxValue < beta) {
					beta = maxValue;
				}
			}

			return minimizingMove;
		}
		
		return move;
	}
}