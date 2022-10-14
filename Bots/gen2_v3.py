import chess
import random
import time
from enum import Enum
import Evaluators.Table.v1 as Table
import Evaluators.Checkmate.v1 as Checkmate
import Evaluators.Pieces.v1 as Pieces
import Evaluators.AttackDefend.v1 as AttactDefend

class Weights(Enum):
    PICES_SCORE = 0
    POSISIONS_SCORE = 1
    IS_DEFENDED = 2
    IS_CHECKMATE = 3

class Bot:
    def __init__(self, weights = [0.8268298942321526, 0.07805562253253272, 0.5324320602889405, 0.6138843173687217]):
        self.name = "Gen2 V02"
        self.numberOfWins = 0.0
        self.Score = 0
        self.weights = weights
        self.color = 0
        self.mean_calc_time = 0.0
        self.total_calc_time = 0.0
        self.number_of_moves = 0.0
        if len(weights) == 0:
            for i in range (0, len(Weights)):
                self.weights.append(1.0)

    def getWeight(self, id):
        if len(self.weights) > id.value:
            return self.weights[id.value]
        else:
            return 1.0

    def setRandomWeights(self):
        self.weights = []
        for i in range(0, len(Weights)):
            self.weights.append(random.uniform(-1, 1))

    def generateNewWeights(self, dist):
        newWeights = []
        for weight in self.weights:
            newWeights.append(weight + random.uniform(-dist, dist))
        return newWeights

    def selectMove(self, board):
        start_time = time.time()
        self.number_of_moves = self.number_of_moves + 1
        # Get legal moves in random order
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)

        bestmove = legal_moves[0]
        self.color = board.turn
        score = -99999999999

        for move in legal_moves:
            board.push(move)
            result = self.__AlphaBetaPruning(board)
            board.pop()
            if result > score:
                score = result
                bestmove = move
        self.total_calc_time = self.total_calc_time + (time.time() - start_time)
        self.mean_calc_time = self.total_calc_time/self.number_of_moves

        return bestmove

    def __AlphaBetaPruning(self, board, depth_left = 3, alpha = -999999, beta = +999999):
        if depth_left == 0:
            return self.__evaluateBoard(board)
        else:
            depth_left = depth_left - 1
            if self.color == board.turn:
                bestScore = -99999999999
                for move in board.legal_moves:
                    board.push(move)
                    score = self.__AlphaBetaPruning(board, depth_left, alpha, beta)
                    board.pop()
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break
                return bestScore
            else:
                worstScore = 99999999999
                for move in board.legal_moves:
                    board.push(move)
                    score = self.__AlphaBetaPruning(board, depth_left, alpha, beta)
                    board.pop()
                    worstScore = min(worstScore, score)
                    beta = min(beta, worstScore)
                    if beta <= alpha:
                        break
                return worstScore

    def __evaluateBoard(self, board):
        ValueOfPiecesScore =   Pieces.evaluateValueOfPiecesScore(board, self.color) * self.getWeight(Weights.PICES_SCORE)
        position_score = Table.evaluatePositions(board, self.color) * self.getWeight(Weights.POSISIONS_SCORE)
        defended_score = AttactDefend.evaluateIfDefended(board, board.move_stack[-1], self.color) * self.getWeight(Weights.IS_DEFENDED)
        checkmate_score = Checkmate.evaluateCheckMate(board, self.color) * self.getWeight(Weights.IS_CHECKMATE)
        return ValueOfPiecesScore + defended_score + checkmate_score + position_score 
