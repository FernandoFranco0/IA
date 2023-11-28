import random

class Q:
    def __init__(self, alpha : float, gamma : float, eps : float, epsDecay=0.001):
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.epsDecay = epsDecay
        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i,j))
        self.Q = {1 : {}, 2 : {}}

    def getAction(self, state : str, playerNum : int, p : bool = False):

        possibleActions = [a for a in self.actions if state[a[0]*3 + a[1]] == '-']
        
        if state not in self.Q[playerNum]:
            self.Q[playerNum][state] = {}
            for action in possibleActions:
                self.Q[playerNum][state][action] = 0

        if random.random() < self.eps:

            action = possibleActions[random.randint(0,len(possibleActions)-1)]
        else:
            values = [self.Q[playerNum][state][a] for a in possibleActions]

            ix_max = [a for a in possibleActions if self.Q[playerNum][state][a] == max(values)  ]

            action = ix_max[random.randint(0, len(ix_max) - 1)]
        
        if p:
            print(self.Q[state])
        return action
    
    def update(self, oldState : str, newState : str, action : tuple[int, int], reward : int, playerNum : int):

        if oldState not in self.Q[playerNum]:
                possibleActions = [a for a in self.actions if oldState[a[0]*3 + a[1]] == '-']
                self.Q[playerNum][oldState] = {}
                for act in possibleActions:
                    self.Q[playerNum][oldState][act] = 0

        
        if newState is not None:
            if newState not in self.Q[playerNum]:
                possibleActions = [a for a in self.actions if newState[a[0]*3 + a[1]] == '-']
                self.Q[playerNum][newState] = {}
                for act in possibleActions:
                    self.Q[playerNum][newState][act] = 0

            possibleActions = [a for a in self.actions if newState[a[0]*3 + a[1]] == '-']
            QValues = [self.Q[playerNum][newState][act] for act in possibleActions]
            
            sample = reward + self.gamma * (max(QValues) if len(QValues) > 0 else 0)
            self.Q[playerNum][oldState][action] = ( 1 - self.alpha ) * self.Q[playerNum][oldState][action] + self.alpha * sample

        else:
            self.Q[playerNum][oldState][action] = reward
        