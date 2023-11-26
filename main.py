from game2 import Game
from q2 import Q2
from td import TD

def play( games : int, agente : Q2,  human ):
    a1 = 0
    a2 = 0
    d = 0

    for _ in range(games):
        game = Game(agente)
        result,player = game.training( human )
        if result == 100 or result == 400:
            d += 1
        elif result == 1000 and player == 1:
            a1 += 1
        else:
            a2 += 1
        if human == 1:
            human = 2
        elif human == 2:
            human = 1

    print(f"Vitorias a1 {a1/games}")
    print(f"Vitorias a2 {a2/games}")
    print(f"Empates {d/games}")
    print()

# training
agente = Q2( 0.001, 1, 1 )

tdAgent = TD( 0.1, 1,1 )
  
print(f"a1 : alpha : {agente.alpha} gamma : {agente.gamma} epsilon : {agente.eps}")

play( 100000, agente, 3 )


# playinh
agente.eps = 0

play( 1000, agente, 3 )




