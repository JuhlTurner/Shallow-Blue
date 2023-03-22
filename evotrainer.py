import random
import os
import sys
import copy
from datetime import datetime

from Bots.gen2_v4 import Bot # import Chess bot
import chess

id = 0

def clearConsole():
    os.system('cls')

def getValueOfPieces(board, player):
    value = len(board.pieces(chess.PAWN, player)) * 1
    value += len(board.pieces(chess.KNIGHT, player)) * 3
    value += len(board.pieces(chess.BISHOP, player)) * 3
    value += len(board.pieces(chess.ROOK, player)) * 5
    value += len(board.pieces(chess.QUEEN, player)) * 9
    return value

def createInitialPub(size):
    bots = []
    for i in range(size):
        bots.append(Bot())
        bots[-1].setRandomWeights()
        bots[-1].comments = False
    return bots

def getScore(bot):
    return bot.numberOfWins

def playGame(student, opponent, numberOfGames):

    studentcolor = chess.WHITE

    for i in range(numberOfGames):        
        studentcolor = not studentcolor
        board = chess.Board()

        while not board.is_game_over():
            playerName = ""
            if board.turn == studentcolor:
                move = student.selectMove(board,0,0)
                playerName = student.name
            else:
                move = opponent.selectMove(board,0,0)
                playerName = opponent.name

            board.push(move)

        if board.result() == "1-0" and studentcolor == chess.WHITE:
            student.numberOfWins += 1
        elif board.result() == "0-1" and studentcolor == chess.BLACK:
            student.numberOfWins += 1
        elif board.result() != "1/2-1/2":
            opponent.numberOfWins += 1

    return student.numberOfWins - opponent.numberOfWins
    
def evaluateBots(bots):
    numberOfCombinations = 0
    numberOfCombinationsCompleate = 0
    for x, bot1 in enumerate(bots):
        for y, bot2 in enumerate(bots):
            if x < y:
                numberOfCombinations = numberOfCombinations + 1
    for x, bot1 in enumerate(bots):
        for y, bot2 in enumerate(bots):
            if x < y:
                numberOfCombinationsCompleate = numberOfCombinationsCompleate + 1
                print ("\t\t%d%% complete" % (float(numberOfCombinationsCompleate)*100/float(numberOfCombinations)), end="\r")
                playGame(bot1,bot2,1)

def sortBots(bots):
    bots.sort(key=getScore, reverse=True)
    for bot in bots:
        bot.numberOfWins = 0

def saveResultsToFile(fileName, bestWeights):
    f = open(fileName, "w")
    for gen, weights in  enumerate(bestWeights):
        f.write("Gen %d: " % (int(gen)+1))
        f.write("%s" % weights)
        f.write("\n")
    f.close()

def evoTrainer(bots, numberOfGens):
    now = datetime.now()
    result_file_name = now.strftime("evotrainer_results_%d%m%Y_%H%M%S.txt")
    bestWeights = []

    for i in range(numberOfGens):
        clearConsole()
        print ("Best Weights:")
        for gen, weights in  enumerate(bestWeights):
            print("\tGen %d:" % (int(gen)+1), end =" ")
            print(weights)
        print("Saving weights to: %s" % result_file_name)

        print("Generation %d of %d" %(i+1,numberOfGens))
        print("\tEvaluating fitness of population ...")
        evaluateBots(bots)
        print("\tSelecting the fittest individuals for reproduction ...")
        sortBots(bots)
        bestWeights.append(copy.deepcopy(bots[0].weights))
        print("\tBreed new individuals and Replace the least-fit individuals of the population ...")
        breedBots(bots)
        print("\tSaving best individual to disk (%s) ..." % result_file_name)
        saveResultsToFile(result_file_name,bestWeights)

    clearConsole()
    print ("Best Weights:")
    f = open("results.txt", "w")
    for gen, weights in  enumerate(bestWeights):
        print("\tGen %d:" % (int(gen)+1), end =" ")
        print(weights)
        f.write(weights)
        f.write("\n")
    print("Saved best weights to: %s" % result_file_name)


def breedBots(bots):
    cutoff = int(len(bots)/4)
    for bot_index, bot in enumerate(bots[cutoff:]):
        bot = Bot()
        for index, weight in enumerate(bot.weights):
            oldval = float(bots[random.randint(0, cutoff-1)].weights[index])
            bots[bot_index].weights[index] = oldval + random.uniform(0.0, 0.1)


def main():
    bots = createInitialPub(10)
    evoTrainer(bots,50)
    
    return
if __name__ == '__main__':
    main()
