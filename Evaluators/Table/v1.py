import chess

PAWN_TABLE = [
      1,  1,  1,  1,  1,  1,  1,  1,
      4,  4,  1,  1,  1,  1,  4,  4,
      1,  1,  3,  1,  1,  3,  1,  1,
      1,  1,  1,  4,  4,  1,  1,  1,
      1,  1,  1,  1,  1,  1,  1,  1,
      5,  5,  5,  5,  5,  5,  5,  5,
      8,  8,  8,  8,  8,  8,  8,  8,
     10, 10, 10, 10, 10, 10, 10, 10,]
    
KNIGHT_TABLE = [
      1,  1,  1,  1,  1,  1,  1,  1,
      1,  3,  3,  3,  3,  3,  3,  1,
      1,  3,  8,  6,  6,  8,  1,  1,
      1,  3,  6,  8,  8,  6,  1,  1,
      1,  3,  6,  8,  8,  6,  1,  1,
      1,  3,  6,  6,  6,  6,  1,  1,
      1,  3,  3,  3,  3,  3,  3,  1,
      1,  1,  1,  1,  1,  1,  1,  1,]

BISHOP_TABLE = [
      1,  1,  1,  1,  1,  1,  1,  1,
      1,  3,  3,  3,  3,  3,  3,  1,
      1,  3,  4,  6,  6,  4,  1,  1,
      1,  3,  6,  6,  6,  6,  1,  1,
      1,  3,  6,  6,  6,  6,  1,  1,
      1,  3,  4,  6,  6,  4,  1,  1,
      1,  3,  3,  3,  3,  3,  3,  1,
      1,  1,  1,  1,  1,  1,  1,  1,]

ROOK_TABLE = [
      1,  1,  1,  2,  2,  1,  1,  1,
      1,  2,  2,  2,  2,  2,  2,  1,
      1,  2,  2,  2,  2,  2,  2,  1,
      1,  2,  2,  2,  2,  2,  2,  1,
      1,  2,  2,  2,  2,  2,  2,  1,
      1,  3,  3,  3,  3,  3,  3,  1,
      1,  3,  3,  3,  3,  3,  3,  1,
      1,  1,  1,  1,  1,  1,  1,  1,]

QUEEN_TABLE = [
      1,  1,  1,  1,  1,  1,  1,  1,
      1,  1,  4,  4,  4,  4,  1,  1,
      1,  4,  8,  8,  8,  8,  4,  1,
      1,  4,  8,  8,  8,  8,  4,  1,
      1,  4,  8,  8,  8,  8,  4,  1,
      1,  4,  8,  8,  8,  8,  4,  1,
      1,  1,  4,  4,  4,  4,  1,  1,
      1,  1,  1,  1,  1,  1,  1,  1,]

KING_TABLE = [
      6,  4,  2,  1,  1,  2,  4,  6,
      1,  1,  1,  1,  1,  1,  1,  1,
      1,  1,  1,  1,  1,  1,  1,  1,
      1,  1,  1,  1,  1,  1,  1,  1,
      1,  1,  1,  1,  1,  1,  1,  1,
      1,  1,  1,  1,  1,  1,  1,  1,
      1,  1,  1,  1,  1,  1,  1,  1,
      1,  1,  1,  1,  1,  1,  1,  1,]


def evaluatePositions(board, player_color):
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
    if player_color == chess.WHITE:
        return score
    else:
        return -score