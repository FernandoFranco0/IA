import random

class TD:
    def __init__(self, alpha : float, gamma : float, eps : float, epsDecay=0.001):
        # Agent parameters
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.epsDecay = epsDecay
        # Possible actions correspond to the set of all x,y coordinate pairs
        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i,j))
        # Initialize Q values to 0 for all state-action pairs.
        # Access value for action a, state s via Q[a][s]
        self.Q = {1 : {}, 2 : {}}

    def getAction(self, state : str, playerNum : int, p : bool = False):
        """
        Select an action given the current game state.
        """
        possibleActions = [a for a in self.actions if state[a[0]*3 + a[1]] == '-']
        
        if state not in self.Q[playerNum]:
            self.Q[playerNum][state] = 0


        # Only consider the allowed actions (empty board spaces)
        if random.random() < self.eps:
            # Random choose.
            action = possibleActions[random.randint(0,len(possibleActions)-1)]
        else:
            # Greedy choose.
            values = []
            for a in possibleActions:
                l = list ( state )
                l[a[0]*3 + a[1]] = "O" if playerNum == 1 else "X"
                newState = ''.join( l )

                if newState not in self.Q[playerNum]:
                    self.Q[playerNum][newState] = 0
                values.append(self.Q[playerNum][newState])

            # Find location of max

            ix_max = []

            for i in range( len(possibleActions) ):
                l = list ( state )
                l[possibleActions[i][0]*3 + possibleActions[i][1]] = "O" if playerNum == 1 else "X"
                newState = ''.join( l )
                
                if self.Q[playerNum][newState] == max(values):
                    ix_max.append(i)

            # If multiple actions were max, then sample from them
            ix_select = ix_max[random.randint(0, len(ix_max) - 1)]

            action = possibleActions[ix_select]
        
        if p:
            print(self.Q[state])
        return action
    
    def update(self, oldState : str, newState : str, action : tuple[int, int], reward : int, playerNum : int):
        """
        Perform the Q-Learning update of Q values.
        """
        # Update Q(s,a)
        if newState is not None:

            if oldState not in self.Q[playerNum]:
                self.Q[playerNum][oldState] = 0

            if newState not in self.Q[playerNum]:
                self.Q[playerNum][newState] = 0


            # update
            sample = reward + self.gamma * self.Q[playerNum][newState]
            self.Q[playerNum][oldState] = ( 1 - self.alpha ) * self.Q[playerNum][oldState] + self.alpha * sample
        else:
            self.Q[playerNum][oldState] = reward