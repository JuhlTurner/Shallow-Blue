from chessbots.v10.bot import Bot # import Chess bot
import chess

def main():
    engine = 0
    board = 0
    exitFlag = False
    while not exitFlag:
        cmds = input().split()

        if cmds[0] == "uci":
            print("id name Super Chess Engine")
            print("id author Stig Turner")
            print("uciok")

        elif cmds[0] == "isready":
            board = chess.Board()
            engine = Bot() # Create Bot
            print("readyok")

        elif cmds[0] == "position":
            if cmds[1] == "startpos":
                board = chess.Board()
                if (len(cmds) > 2) and (cmds[2] == "moves"):
                    for i in range(3, len(cmds)):
                        board.push_uci(cmds[i])
                else:
                    board = chess.Board()
                move = engine.selectMove(board) # make a move 
                print("bestmove " + move.uci())

        elif cmds[0] == "quit":
            print("Bye.")
            exitFlag = True
        else:
            print("info string Received unknown cmds: %s" % str(cmds))

if __name__ == '__main__':
    main()