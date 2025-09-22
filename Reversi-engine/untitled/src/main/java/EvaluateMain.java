import java.util.LinkedList;

public class EvaluateMain {
    public static void main(String[] args) {
        EdaxStyleEvaluator eval = new EdaxStyleEvaluator();
        RankedEvaluator eval2 = new RankedEvaluator();
        OthelloPosition pos = new OthelloPosition("BOOOOOOOOOOOOOOOEOOOOOOOOOOOOOEOEOOOOXXXEOOOOOOEEOEXEOEEEOEEOOOEE");
        LinkedList<OthelloAction> s = pos.getMoves();
        for (OthelloAction action : s) {
            OthelloPosition pos2 = pos.clone();
            pos2.makeMove(action);
            action.print();
            System.out.println("Value1: " + eval.evaluate(pos2));
            System.out.println("Value2: " + eval2.evaluate(pos2));

        }
    }
}
