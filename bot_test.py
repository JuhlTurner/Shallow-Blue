import chess
import os

from Bots.gen2_v3 import Bot as Student
from Bots.gen1_v10 import Bot as Opponent
import Evaluators.Pieces.v1 as Pieces

def clearConsole():
    os.system('cls')


def evoTrainer():
    numberOfVariants = 50
    numberOfGames = 20
    numberOfGenerations = 10
    variants = []

    #generate initial population
    for j in range(numberOfVariants):
        variants.append(Student())
        variants[-1].setRandomWeights()


def playGame(student, opponent, numberOfGames):

    studentcolor = chess.WHITE

    for i in range(numberOfGames):        
        #studentcolor = not studentcolor
        board = chess.Board()

        while not board.is_game_over():
            playerName = ""
            if board.turn == studentcolor:
                move = student.selectMove(board)
                playerName = student.name
            else:
                move = opponent.selectMove(board)
                playerName = opponent.name

            board.push(move)
            clearConsole()
            student.totalScore = Pieces.getValueOfPieces(board, studentcolor)
            opponent.totalScore = Pieces.getValueOfPieces(board, not studentcolor)
            print("Game %d of %d" % (i+1, numberOfGames))
            print(board)
            print("Score:\n\t%s: %d (Wins: %d, mean move time: %s) \n\t%s: %d (Wins: %d, mean move time: %s)" % (student.name, student.totalScore, student.numberOfWins, student.mean_calc_time, opponent.name, opponent.totalScore, opponent.numberOfWins, opponent.mean_calc_time))

        if board.result() == "1-0" and studentcolor == chess.WHITE:
            student.numberOfWins += 1
        elif board.result() == "0-1" and studentcolor == chess.BLACK:
            student.numberOfWins += 1
        elif board.result() != "1/2-1/2":
            opponent.numberOfWins += 1
       
        clearConsole()
        print("Game %d of %d" % (i+1, numberOfGames))
        print(board)
        print("Score:\n\t%s: %d (Wins: %d) \n\t%s: %d (Wins: %d)" % (student.name, student.totalScore, student.numberOfWins, opponent.name, opponent.totalScore, opponent.numberOfWins))
        #print("Calulating move for %s..." % playerName)

    return student.numberOfWins - opponent.numberOfWins
    
def main():
    playGame(Student(),Opponent(),20)
    return

    
    #evoTrainer()
    #return
    player1 = BotV5()
    player2 = BotV6()
    whitePlayer = player1
    blackPlayer = player2

    numberOfGames = 100

    for i in range(numberOfGames):
        tmp = whitePlayer
        whitePlayer = blackPlayer
        blackPlayer = tmp
        board = chess.Board()
        while not board.is_game_over():
            if board.turn == chess.WHITE:
                move = whitePlayer.selectMove(board)
            else:
                move = blackPlayer.selectMove(board)

            board.push(move)


            #clearConsole()
            #print(board)
            #print("Score:\n\t%s: %d \n\t%s: %d" % (player1.name, player1.totalScore, player2.name, player2.totalScore))

            if board.result() == "1-0":
                print(board)
                whitePlayer.numberOfWins += 1
            elif board.result() == "0-1":
                print(board)
                blackPlayer.numberOfWins += 1
            #elif board.result() == "1/2-1/2":
            #   whitePlayer.numberOfWins += 0.5
            #  blackPlayer.numberOfWins += 0.5
            
            whitePlayer.totalScore = getValueOfPieces(board, chess.WHITE)
            blackPlayer.totalScore = getValueOfPieces(board, chess.BLACK)
            clearConsole()
            print(board)
            print("Score:\n\t%s: %d (Wins: %d) \n\t%s: %d (Wins: %d)" % (player1.name, player1.totalScore, player1.numberOfWins, player2.name, player2.totalScore, player2.numberOfWins))

        clearConsole()
        totalScore = player1.totalScore + player2.totalScore
        player1ScorePct = round(float(player1.totalScore)/float(totalScore)*100.0)
        player2ScorePct = 100 - player1ScorePct
        print("Game %d of %d" % (i+1, numberOfGames))
        #print(board)
        print("Score:\n\t%s: %d (%d%%, Wins: %d) \n\t%s: %d (%d%%, Wins: %d)" % (player1.name, player1.totalScore, player1ScorePct, player1.numberOfWins, player2.name, player2.totalScore, player2ScorePct,  player2.numberOfWins))
    return
if __name__ == '__main__':
    main()

