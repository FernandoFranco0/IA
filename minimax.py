import random


class Minimax:
    def __init__(self, depth):
        self.depth = depth
        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i,j))

    def checkForWin(self, state : str, key : str):
        # check for player win on diagonals
        a = [state[0], state[4], state[8]]
        b = [state[2], state[4], state[6]]
        if a.count(key) == 3 or b.count(key) == 3:
            return True
        # check for player win on rows/columns
        for i in range(3):
            col = [state[i], state[3 + i], state[6 + i]]
            row = [state[3 * i], state[3 * i + 1], state[3 * i + 2]]
            if col.count(key) == 3 or row.count(key) == 3:
                return True
        return False

    def getAction(self, state : str, playerNum : int):
        if state.count("-") == 9:
            #return random.choice(self.actions)
            return (0,0)
        value, action = self.minimax(state, self.depth, playerNum)
        return action

    def minimax(self, state : str, depth : int, playerNum : int, isMaximizing = True):
        if state.count("-") == 0:
            return (0.1 if playerNum == 1 else 0.4), None
        
        if self.checkForWin(state, "O" if playerNum == 1 else "X"):
            return 1, None
        
        if self.checkForWin(state, "X" if playerNum == 1 else "O"):
            return 0, None
        
        if depth == 0:
            return 0, None

        possibleActions = [a for a in self.actions if state[a[0]*3 + a[1]] == '-']
        
        if isMaximizing:
            max = -float("inf")

            for a in possibleActions:
                l = list ( state )
                l[a[0]*3 + a[1]] = "O" if playerNum == 1 else "X"
                newState = ''.join( l )
                value, _ = self.minimax(newState, depth-1, 2 if playerNum == 1 else 1, not isMaximizing)
                if value >= max:
                    max = value
                    action = a
        else:
            max = float("inf")

            for a in possibleActions:
                l = list ( state )
                l[a[0]*3 + a[1]] = "O" if playerNum == 1 else "X"
                newState = ''.join( l )
                value, _ = self.minimax(newState, depth-1, 2 if playerNum == 1 else 1, not isMaximizing)
                if value <= max:
                    max = value
                    action = a

        return max, action

    def update(self, oldState : str, newState : str, action : tuple[int, int], reward : int, playerNum : int):
        pass
