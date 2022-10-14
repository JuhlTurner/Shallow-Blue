import chess
def evaluateCheckMate(board, player_coler):
    if board.is_checkmate() and board.turn != player_coler:
        return 5
    elif board.is_checkmate():
        return -5
    else:
        return 0
