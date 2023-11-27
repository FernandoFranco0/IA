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

    def training(self, humam):
        playerNum = 1
        opponentNum = 2
        move = 1

        # iterate until game is over
        while True:

            state = getStateKey(self.board)
            if playerNum != humam:
                action = self.agentPair[playerNum-1].getAction(state, playerNum)
            else:
                printBoard(state, move)
                x = int(input())
                y = int(input())
                action = (x,y)
    
            move += 1

            # execute oldAction, observe reward and state
            self.board[action[0]][action[1]] = 'O' if playerNum == 1 else 'X'

            check = self.checkForEnd('O' if playerNum == 1 else 'X')

            newState = getStateKey(self.board)

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
            
            
            # update Q-values
            self.agentPair[0].update(state, newState, action, myReward, playerNum)
            self.agentPair[0].update(state, newState, action, opponentReward, opponentNum)

            if type(self.agentPair[0]).__name__ != type(self.agentPair[1]).__name__:
                self.agentPair[1].update(state, newState, action, myReward, playerNum)
                self.agentPair[1].update(state, newState, action, opponentReward, opponentNum)

            playerNum, opponentNum = opponentNum, playerNum

        # Game over. Perform final update
        if humam == 1 or humam == 2:
            printBoard(getStateKey(self.board), move)

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
    """
    Prints the game board as text output to the terminal.

    Parameters
    ----------
    board : list of lists
        the current game board
    """
    print(f" Jogada {int( move/2 ) + 1} do jogador {move%2} : '{'O' if move%2 == 1 else 'X'}'")
    print('    0   1   2\n')
    for i in range(3):
        print('%i   ' % i, end='')
        for elt in range(3):
            print('%s   ' % board[i * 3 + elt], end='')
        print('\n')
    print()

def getStateKey(board):
    """
    Converts 2D list representing the board state into a string key
    for that state. Keys are used for Q-value hashing.

    Parameters
    ----------
    board : list of lists
        the current game board
    """
    key = ''
    for row in board:
        for elt in row:
            key += elt
    return key