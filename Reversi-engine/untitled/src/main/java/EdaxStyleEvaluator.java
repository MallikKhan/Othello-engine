public class EdaxStyleEvaluator implements OthelloEvaluator {

    @Override
    public int evaluate(OthelloPosition pos) {
        int mobility = mobilityScore(pos);
        int corners = cornerScore(pos);
        int stability = stabilityScore(pos);
        int edges = edgeScore(pos);

        // Example weights (you can tune them):
        return  10 * mobility
                + 25 * corners
                +  5 * stability
                +  3 * edges;
    }

    private int mobilityScore(OthelloPosition pos) {
        // difference in legal moves between players
        pos.maxPlayer = true;
        int whiteMoves = pos.getMoves().size();
        pos.maxPlayer = false;
        int blackMoves = pos.getMoves().size();
        return whiteMoves - blackMoves;
    }

    private int cornerScore(OthelloPosition pos) {
        int N = OthelloPosition.BOARD_SIZE;
        char[][] b = pos.board;
        int score = 0;
        int[][] corners = {{1,1}, {1,N}, {N,1}, {N,N}};
        for (int[] c : corners) {
            if (b[c[0]][c[1]] == 'W') score++;
            else if (b[c[0]][c[1]] == 'B') score--;
        }
        return score;
    }

    private int stabilityScore(OthelloPosition pos) {
        // stable discs (very rough approximation: corners + discs in filled edges)
        int score = 0;
        // TODO: implement full stability calculation
        return score;
    }

    private int edgeScore(OthelloPosition pos) {
        int score = 0;
        int N = OthelloPosition.BOARD_SIZE;
        char[][] b = pos.board;
        for (int i = 1; i <= N; i++) {
            if (b[1][i] == 'W') score++;
            else if (b[1][i] == 'B') score--;
            if (b[N][i] == 'W') score++;
            else if (b[N][i] == 'B') score--;
            if (b[i][1] == 'W') score++;
            else if (b[i][1] == 'B') score--;
            if (b[i][N] == 'W') score++;
            else if (b[i][N] == 'B') score--;
        }
        return score;
    }
}
