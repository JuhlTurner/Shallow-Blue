import chess

def evaluateIfDefended(board, move, player_color):
    if board.is_attacked_by(player_color, move.to_square) and not board.is_attacked_by(not player_color, move.to_square):
        return 2.0
    elif board.is_attacked_by(player_color, move.to_square) or not board.is_attacked_by(not player_color, move.to_square):
        return 1.0
    else:
        return 0.0