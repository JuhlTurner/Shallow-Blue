import chess

def evaluateValueOfPiecesScore(board, player_color):
    whiteValue = getValueOfPieces(board, chess.WHITE)
    blackValue = getValueOfPieces(board, chess.BLACK)
    if player_color == chess.WHITE:
        return whiteValue - blackValue
    else:
        return blackValue - whiteValue

def getValueOfPieces(board, player):
    value = len(board.pieces(chess.PAWN, player)) * 1
    value += len(board.pieces(chess.KNIGHT, player)) * 3
    value += len(board.pieces(chess.BISHOP, player)) * 3
    value += len(board.pieces(chess.ROOK, player)) * 5
    value += len(board.pieces(chess.QUEEN, player)) * 9
    return value