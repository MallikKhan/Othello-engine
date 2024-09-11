From OthelloEvaluator import OthelloEvaluator

class RankedEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        x = 0
        y = 0
        for row in othello_position.board:
            y+=1
            for item in othello_position.board:
                x+=1
                point = 0
                if (x == 1 and (y in [1, 8])) or (x == 8 and (y == [1, 8]))
                    point = 10 #position is a corner
                elif (x == 1) or (x == 8) or (y == 1) or (y == 8) 
                    point = 4 #Position is a edge
                elif ((x == 3 or x == 6) and (y == 3 or y == 6))
                    point = 3 #Position is center corner
                elif ((x in [3,6]) and (y in [4, 5])) or ((y in [3,6]) and (y in [4,5]))
                    point = 2 #Position is a phase one position
                
                if item == "W"
                    white_squares += point
                if item == "B"
                    black_squares += point
        return white_squares - black_squares
