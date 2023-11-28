import random

from q import Q

class Game:
    def __init__(self, agent, agent2):
        self.agentPair = (agent,agent2)
        # initialize the game board
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def checkForWin(self, key):
        # check for player win on diagonals
        a = [self.board[0][0], self.board[1][1], self.board[2][2]]
        b = [self.board[0][2], self.board[1][1], self.board[2][0]]
        if a.count(key) == 3 or b.count(key) == 3:
            return True
        # check for player win on rows/columns
        for i in range(3):
            col = [self.board[0][i], self.board[1][i], self.board[2][i]]
            row = [self.board[i][0], self.board[i][1], self.board[i][2]]
            if col.count(key) == 3 or row.count(key) == 3:
                return True
        return False

    def checkForDraw(self):
        draw = True
        for row in self.board:
            for elt in row:
                if elt == '-':
                    draw = False
        return draw

    def checkForEnd(self, key : str):
        if self.checkForWin(key):
            return 1000
        elif self.checkForDraw():
            return 0
        return -1000

    def training(self, humam, p = False):
        playerNum = 1
        opponentNum = 2
        move = 1
        if p:
            printBoard(getState(self.board), move)

        while True:

            state = getState(self.board)
            
            if playerNum != humam:
                action = self.agentPair[playerNum-1].getAction(state, playerNum)
            else:
                print("Nao e checado se a sua jogada e valida, i.e. se a casa esta vazia")
                print("Digite a linha da sua jogada em um linha e a coluna da sua jogada em outra: ")
                x = int(input())
                y = int(input())
                action = (x,y)
            
            move += 1

            self.board[action[0]][action[1]] = 'O' if playerNum == 1 else 'X'

            check = self.checkForEnd('O' if playerNum == 1 else 'X')

            newState = getState(self.board)

            if p:
                printBoard(newState, move)                

            if not check == -1000:
                if check == 1000:
                    myReward = check 
                    opponentReward = -check
                else:
                    myReward = 100 if playerNum == 1 else 400
                    opponentReward = 400 if playerNum == 1 else 100
                break
            else:
                myReward = 0
                opponentReward = 0
            
            self.agentPair[0].update(state, newState, action, myReward, playerNum)
            self.agentPair[0].update(state, newState, action, opponentReward, opponentNum)

            if type(self.agentPair[0]).__name__ != type(self.agentPair[1]).__name__:
                self.agentPair[1].update(state, newState, action, myReward, playerNum)
                self.agentPair[1].update(state, newState, action, opponentReward, opponentNum)

            playerNum, opponentNum = opponentNum, playerNum

        if p:
            printBoard(getState(self.board), move)

        self.agentPair[0].update(newState, None, action, myReward, playerNum)
        self.agentPair[0].update(state, newState, action, myReward, playerNum)

        self.agentPair[0].update(newState, None, action, opponentReward, opponentNum)
        self.agentPair[0].update(state, newState, action, opponentReward, opponentNum)
        
        if type(self.agentPair[0]).__name__ != type(self.agentPair[1]).__name__:
            self.agentPair[1].update(newState, None, action, myReward, playerNum)
            self.agentPair[1].update(state, newState, action, myReward, playerNum)

            self.agentPair[1].update(newState, None, action, opponentReward, opponentNum)
            self.agentPair[1].update(state, newState, action, opponentReward, opponentNum)

        return myReward, playerNum
    

def printBoard(board, move = 0):
    print()
    print('    0   1   2\n')
    for i in range(3):
        print('%i   ' % i, end='')
        for elt in range(3):
            print('%s   ' % board[i * 3 + elt], end='')
        print('\n')
    print(f" Jogada {int( (move+1)/2 )} do jogador {2 - move%2} : '{'O' if move%2 == 1 else 'X'}'")

def getState(board):
    key = ''
    for row in board:
        for elt in row:
            key += elt
    return key