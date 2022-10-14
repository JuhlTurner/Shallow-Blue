from unittest import result
import chess
import time
from multiprocessing import freeze_support
from random import randint
import random
import os
import sys

from numpy import number
from chessbots.v8.bot import Bot as BotV10

from chessbots.v11.bot import Bot as Student
from chessbots.v10.bot import Bot as Opponent

import plotext as plt

def clearConsole():
    os.system('cls')

def getValueOfPieces(board, player):
    value = len(board.pieces(chess.PAWN, player)) * 1
    value += len(board.pieces(chess.KNIGHT, player)) * 3
    value += len(board.pieces(chess.BISHOP, player)) * 3
    value += len(board.pieces(chess.ROOK, player)) * 5
    value += len(board.pieces(chess.QUEEN, player)) * 9
    return value

def getScore(bot):
    return bot.Score


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
            student.totalScore = getValueOfPieces(board, studentcolor)
            opponent.totalScore = getValueOfPieces(board, not studentcolor)
            print("Game %d of %d" % (i+1, numberOfGames))
            print(board)
            print("Score:\n\t%s: %d (Wins: %d) \n\t%s: %d (Wins: %d)" % (student.name, student.totalScore, student.numberOfWins, opponent.name, opponent.totalScore, opponent.numberOfWins))

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
    playGame(Student(),Opponent(),10)
    return
if __name__ == '__main__':
    main()

