import random

from q2 import Q2

class Game:
    def __init__(self, agent : Q2):
        self.agent = agent
        # initialize the game board
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def checkForWin(self, key):
        """
        Check to see whether the player/agent with token 'key' has won.
        Returns a boolean holding truth value.

        Parameters
        ----------
        key : string
            token of most recent player. Either 'O' or 'X'
        """
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
        """
        Checks if player/agent with token 'key' has ended the game. Returns -1
        if the game is still going, 0 if it is a draw, and 1 if the player/agent
        has won.

        Parameters
        ----------
        key : string
            token of most recent player. Either 'O' or 'X'
        """
        if self.checkForWin(key):
            return 1000
        elif self.checkForDraw():
            return 0
        return -1000

    def training(self):
        playerTurn = 1
        state = getStateKey(self.board)
        self.agent.getAction(state, playerTurn)
        # iterate until game is over
        while True:
            # execute oldAction, observe reward and state
            self.board[action1[0]][action1[1]] = 'O'

            check = self.checkForEnd('O')

            if not check == -1:
                # game is over. +1 reward if win, 0 if draw
                reward = check
                break
            else:
                reward = 0

            if not firstIt:
                newState2 = getStateKey(self.board)
                

            firstIt = False

            state2 = getStateKey(self.board)
            action2 = self.agent2.getAction(state2, False)
            self.board[action2[0]][action2[1]] = 'X'

            check = self.checkForEnd('X')

            if not check == -1:
                # game is over. -1 reward if lose, 0 if draw
                reward = -1*check
                #print( "Draw" if check == 0 else "Agent2 won" )
                break
            else:
                # game continues. 0 reward
                reward = 0

            newState = getStateKey(self.board)

            # update Q-values
            self.agent.update(state1, newState, action1, reward)
            self.agent2.update(state2, newState, action2, -reward)

            state1 = newState
            action1 = self.agent.getAction(state1, False)

        # Game over. Perform final update

        self.agent.update(state1, None, action1, reward)

        self.agent2.update(state2, None, action2, -reward)

        return reward
    
    def play(self, print : bool):
        move = 1
        state1 = getStateKey(self.board)
        action1 = self.agent.getAction(state1, False)

        while True:
            
            # execute oldAction, observe reward and state
            self.board[action1[0]][action1[1]] = 'O'
            
            move += 1
            if print:
                printBoard(getStateKey(self.board), move)

            check = self.checkForEnd('O')
            
            if not check == -1:
                # game is over. +1 reward if win, 0 if draw
                reward = check * 1000
                #print( "Draw" if check == 0 else "Agent1 won" )
                break

            state2 = getStateKey(self.board)
            action2 = self.agent2.getAction(state2, False)
            self.board[action2[0]][action2[1]] = 'X'

            check = self.checkForEnd('X')

            move += 1
            if print:
                printBoard(getStateKey(self.board), move)

            if not check == -1:
                # game is over. -1 reward if lose, 0 if draw
                reward = -1*check * 1000
                break
            else:
                # game continues. 0 reward
                reward = 0
            newState = getStateKey(self.board)

            # update Q-values
            state1 = newState
            action1 = self.agent.getAction(state1, False)

        # Game over. Perform final update
        

        return reward

def printBoard(board, move):
    """
    Prints the game board as text output to the terminal.

    Parameters
    ----------
    board : list of lists
        the current game board
    """
    print(f" Jogada {int( move/2 )} do jogador {move%2 + 1}")
    print('    0   1   2\n')
    for i in range(3):
        print('%i   ' % i, end='')
        for elt in range(3):
            print('%s   ' % board[i * 3 + elt], end='')
        print('\n')
    print()
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