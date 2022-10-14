import chess
import random
from enum import Enum
from functools import partial
from chessbots.v9.pieceTables import PAWN_TABLE, KNIGHT_TABLE, BISHOP_TABLE, ROOK_TABLE, QUEEN_TABLE, KING_TABLE 

class Weights(Enum):
    PICES_SCORE = 0
    POSISIONS_SCORE = 1
    IS_DEFENDED = 2
    IS_CHECKMATE = 3

class Bot:
    def __init__(self, weights = [0.8268298942321526, 0.07805562253253272, 0.5324320602889405, 0.6138843173687217]):
        self.name = "Gen1 V10"
        self.numberOfWins = 0.0
        self.Score = 0
        self.weights = weights
        self.color = 0
        self.mean_calc_time = 0.0
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
        bestmove = random.choice(list(board.legal_moves))
        self.color = board.turn
        score = 0
        for move in list(board.legal_moves):
            board.push(move)
            result = self.__evaluateBoardDepth(board)
            board.pop()
            if result > score:
                score = result
                bestmove = move
        return bestmove

    #def evaluateBoard(self, move, board, turn):
    #        bestScore = 0
    #        turn = board.turn
    #        for move in board.legal_moves:
    #            board.push(move)
    #            score = self.evaluateBoardDepth(board,turn)
    #            board.pop()
    #            if score > bestScore:
    #                bestScore = score
    #        return bestScore

    def __evaluateBoardDepth(self, board, depth_left = 2):
        if depth_left == 0:
            return self.__evaluateBoard(board)
        else:
            if self.color == board.turn:
                bestScore = -99990
            else:
                bestScore = 99999
            for move in board.legal_moves:
                board.push(move)
                score = self.__evaluateBoardDepth(board, depth_left - 1)
                board.pop()
                if self.color == board.turn and score > bestScore:
                    bestScore = score
                elif self.color != board.turn and score < bestScore:
                    bestScore = score
            return bestScore


    def __evaluateBoard(self, board):
        ValueOfPiecesScore = self.__evaluateValueOfPiecesScore(board) * self.getWeight(Weights.PICES_SCORE)
        position_score = self.__evaluatePositions(board) * self.getWeight(Weights.POSISIONS_SCORE)
        defended_score = self.__evaluateIfDefended(board, board.move_stack[-1]) * self.getWeight(Weights.IS_DEFENDED)
        checkmate_score = self.__evaluateCheckMate(board) * self.getWeight(Weights.IS_CHECKMATE)
        return ValueOfPiecesScore + defended_score + checkmate_score + position_score 


    def __evaluateIfDefended(self, board,  move):
        if board.is_attacked_by(self.color, move.to_square) and not board.is_attacked_by(not self.color, move.to_square):
            return 5.0
        elif board.is_attacked_by(self.color, move.to_square) or not board.is_attacked_by(not self.color, move.to_square):
            return 2.5
        else:
            return 0.0

    
    def __evaluateCheckMate(self, board):
        if board.is_checkmate() and board.turn != self.color:
            return 5
        elif board.is_checkmate():
            return -5
        else:
            return 0


    ##======================TABLE LOOKUP=====================##

    def __evaluatePositions(self, board):
        score = 0.0
        score += sum([PAWN_TABLE[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        score -= sum([PAWN_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])

        score += sum([KNIGHT_TABLE[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)]) * 3
        score -= sum([KNIGHT_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)]) * 3

        score += sum([BISHOP_TABLE[i] for i in board.pieces(chess.BISHOP, chess.WHITE)]) * 3
        score -= sum([BISHOP_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)]) * 3
    
        score += sum([ROOK_TABLE[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) * 5
        score -= sum([ROOK_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)]) * 5

        score += sum([QUEEN_TABLE[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) * 9
        score -= sum([QUEEN_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)]) * 9

        score += sum([KING_TABLE[i] for i in board.pieces(chess.KING, chess.WHITE)]) * 4
        score -= sum([KING_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)]) * 4
        if self.color == chess.WHITE:
            return score
        else:
            return -score


            
    ##=================VALUE OF PIECES SCORE==================##

    def __evaluateValueOfPiecesScore(self, board):
        whiteValue = self.__getValueOfPieces(board, chess.WHITE)
        blackValue = self.__getValueOfPieces(board, chess.BLACK)
        if self.color == chess.WHITE:
         return whiteValue - blackValue
        else:
            return blackValue - whiteValue

    def __getValueOfPieces(self, board, player):
        value = len(board.pieces(chess.PAWN, player)) * 1
        value += len(board.pieces(chess.KNIGHT, player)) * 3
        value += len(board.pieces(chess.BISHOP, player)) * 3
        value += len(board.pieces(chess.ROOK, player)) * 5
        value += len(board.pieces(chess.QUEEN, player)) * 9
        return value

    ##========================================================##

