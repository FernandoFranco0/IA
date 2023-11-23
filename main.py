from game import Game
from q import Q

def training( games : int, agente1 : Q, agente2 : Q ):
    a1 = 0
    a2 = 0
    d = 0

    for _ in range(games):
        game = Game(agente1, agente2)
        result = game.training()
        if result == 1000:
            a1 += 1
        elif result == -1000:
            a2 += 1
        else:
            d += 1

    print(f"Vitorias a1 {a1/games}")
    print(f"Vitorias a2 {a2/games}")
    print(f"Empates {d/games}")
    print()

def playing( games : int, agente1 : Q, agente2 : Q , board : bool):
    #playing
    agente1.eps = 0
    agente2.eps = 0
    a1 = 0
    a2 = 0
    d = 0
    for i in range(games):
        game = Game(agente1, agente2)
        result = game.play( board )
        if result == 1000:
            a1 += 1
        elif result == -1000:
            a2 += 1
        else:
            d += 1
# o o -
# x x -
# x 0 -
    print("playing results")
    print(f"Vitorias a1 {a1}")
    print(f"Vitorias a2 {a2}")
    print(f"Empates {d}")
    print()

# training
agente1 = Q( 0.5, 1, 1 )  
agente2 = Q( 0.5, 1, 1 )  

print(f"a1 : alpha : {agente1.alpha} gamma : {agente1.gamma} epsilon : {agente1.eps}")
print(f"a2 : alpha : {agente2.alpha} gamma : {agente2.gamma} epsilon : {agente2.eps}")

games = 10000
training( games, agente1, agente2 )
#print("Invertendo ordem de jogadas",end="\n\n")
#training( games, agente2, agente1 )

print("Fazendo melhor jogada sempre", end="\n\n")
playing( 1, agente1, agente2 , True )
