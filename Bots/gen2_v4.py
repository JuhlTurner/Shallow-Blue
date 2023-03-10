import chess
import random
import time
import threading
from enum import Enum
import Evaluators.Table.v1 as Table
import Evaluators.Checkmate.v1 as Checkmate
import Evaluators.Pieces.v1 as Pieces
import Evaluators.AttackDefend.v1 as AttactDefend
import Jokes.v1 as Jokes

class Weights(Enum):
    PICES_SCORE = 0
    POSISIONS_SCORE = 1
    IS_DEFENDED = 2
    IS_CHECKMATE = 3

class Bot:
    def __init__(self, weights = [0.8268298942321526, 0.07805562253253272, 0.5324320602889405, 0.6138843173687217]):
        self.name = "Gen2 V04"
        self.numberOfWins = 0.0
        self.Score = 0
        self.weights = weights
        self.color = 0
        self.mean_calc_time = 0.0
        self.total_calc_time = 0.0
        self.last_move_calc_time = 0.0
        self.number_of_moves = 0.0
        self.insultPrinted = False;
        self.badExcusesPrinted = False;
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

    def getDepthFromTime(self, time_left, opponent_time_left):
        if int(time_left) == 0 or int(opponent_time_left) == 0:
            return 4

        if int(time_left) < 1500:
            return 2
        
        if int(time_left) < 4000:
            return 3
        
        if (int(time_left) - int(opponent_time_left)) > 10000:
            if int(time_left) > 60000:
                return 5

        return 4

    def selectMove(self, board, wtime, btime):
        if self.number_of_moves == 0.0:
            Jokes.connectToAmazonWebServices()

        joke_told = Jokes.tellJoke();
        start_time = time.time()
        self.number_of_moves = self.number_of_moves + 1
        # Get legal moves in random order
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)

        bestmove = legal_moves[0]
        self.color = board.turn
        score = -99999999999

        depth = 4
        if self.color == chess.WHITE:
            depth = self.getDepthFromTime(wtime,btime)
        else:
            depth = self.getDepthFromTime(btime,wtime)
        print("info string %d" % depth)

        score, bestmove = self.__AlphaBetaPruning(board, depth)

        if score < 100000 and not self.insultPrinted and not joke_told:
            if print(Jokes.insult()):
                self.insultPrinted = True

        if score > 100000 and not self.badExcusesPrinted and not joke_told:
            if print(Jokes.badExcuse()):
                self.badExcusesPrinted = True
        self.last_move_calc_time = (time.time() - start_time)
        self.total_calc_time = self.total_calc_time + self.last_move_calc_time
        self.mean_calc_time = self.total_calc_time/self.number_of_moves
        return bestmove

    def __AlphaBetaPruning(self, board, depth_left, alpha = -999999, beta = +999999):
        if depth_left == 0:
            return self.__evaluateBoard(board), board
        else:
            depth_left = depth_left - 1
            if self.color == board.turn:
                bestMove = None
                bestScore = -99999999999
                for move in board.legal_moves:
                    board.push(move)
                    score, unused = self.__AlphaBetaPruning(board, depth_left, alpha, beta)
                    board.pop()
                    if(bestScore < score):
                        bestScore = score
                        bestMove = move
                    #bestScore = max(bestScore, score)
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break
                return bestScore, bestMove
            else:
                worstMove = None
                worstScore = 99999999999
                for move in board.legal_moves:
                    board.push(move)
                    score, unused = self.__AlphaBetaPruning(board, depth_left, alpha, beta)
                    board.pop()
                    #worstScore = min(worstScore, score)
                    if(worstScore > score):
                        worstScore = score
                        worstMove = move
                    beta = min(beta, worstScore)
                    if beta <= alpha:
                        break
                return worstScore, worstMove

    def __evaluateBoard(self, board):
        ValueOfPiecesScore =   Pieces.evaluateValueOfPiecesScore(board, self.color) * self.getWeight(Weights.PICES_SCORE)
        position_score = Table.evaluatePositions(board, self.color) * self.getWeight(Weights.POSISIONS_SCORE)
        defended_score = AttactDefend.evaluateIfDefended(board, board.move_stack[-1], self.color) * self.getWeight(Weights.IS_DEFENDED)
        checkmate_score = Checkmate.evaluateCheckMate(board, self.color) * self.getWeight(Weights.IS_CHECKMATE)
        return ValueOfPiecesScore + defended_score + checkmate_score + position_score 
