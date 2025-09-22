public class Othello {
    public static void main(String[] args) {
        OthelloPosition position = new OthelloPosition();
        int timeLimit = 5; // default

        if (args.length >= 2) {
            position = new OthelloPosition(args[0]);
            timeLimit = Integer.parseInt(args[1])*1000;
        } else {
            position.initialize();
        }

        AlphaBeta alphaBeta = new AlphaBeta(new RankedEvaluator());
        OthelloAction bestMove = new OthelloAction(0, 0);
        OthelloAction previousMove = new OthelloAction(0, 0);
        alphaBeta.setTime(timeLimit, System.currentTimeMillis());
        int depth = 9;
        int repeats = 0;
        long startTime = System.currentTimeMillis();
        while ((System.currentTimeMillis() - startTime) < timeLimit && repeats < 15) {
            alphaBeta.setSearchDepth(depth++);
            bestMove = alphaBeta.evaluate(position);

            if (bestMove.isPassMove() || bestMove.equals(previousMove)) ++repeats;
            else repeats = 0;
            previousMove = bestMove;
        }

        bestMove.print();
    }
}
