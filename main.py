import time
from game2 import Game
from minimax import Minimax
from q import Q
from td import TD
import multiprocessing 
import pickle

def Compare( games, type = "all", type2 = "all", step = 0.1):
    start_time = time.time()

    types = ["TD", "Q", "MN"]
    types2 = ["TD", "Q", "MN"]

    if type != "all":
        types = [type]
    if type2 != "all":
        types2 = [type2]

    processes = []
    for t in types:
        for t2 in types2:
            end = 11 
            if t == "MN":
                end = 2
            for i in range( 1, end ):
                fileName = f"C:/Users/Fernando Franco/Desktop/Comparações{t}{t2}{i}.csv"
                with open(fileName, 'w', encoding='utf-8') as file:
                    file.write(f"Agente 1, {t}, Agente 2, {t2}\n")
                    begin = "Alpha 1, Gamma 1, Epsilon 1, "
                    middle = "Alpha 2, Gamma 2, Epsilon 2, "
                    if t == "MN":
                        begin = "Profundidade, "
                    if t2 == "MN":
                        middle = "Profundidade, "
                    file.write(f"{begin}{middle}Partidas,Partidas Vencidas por 1,Partidas Vencidas por 2,Empates\n")
                p = multiprocessing.Process(target=compMp, args=(i, t, t2, fileName, step, games,))
                processes.append(p)
                p.start()

    for process in processes:
        process.join()

    print("--- %s seconds ---" % (time.time() - start_time))

def compMp( i, type, type2, fileName, step, games ):

    if type == "TD":
        agente = TD( 0, 0, 0 )
    elif type == "Q":
        agente = Q( 0, 0, 0 )
    elif type == "MN":
        agente = Minimax( i )

    if type2 == "TD":
        agente2 = TD( 0, 0, 0 )
    elif type2 == "Q": 
        agente2 = Q( 0, 0, 0 )
    elif type2 == "MN":
        agente2 = Minimax( i )

    print(f"Começando {type} contra {type2} i = {i}...")

    if type != "MN" and type2 != "MN":
        agente.alpha = i * step
        for j in range( int( 1/step + 1 ) ):
            agente.gamma = j * step
            print(f"j = {j}")
            for k in range( int( 1/step + 1 ) ):
                agente.eps = k * step
                for l in range( int( 1/step + 1 ) ):
                    agente2.alpha = l * step
                    for m in range( int( 1/step + 1 ) ):
                        agente2.gamma = m * step
                        for n in range( int( 1/step + 1 ) ):
                            agente2.eps = n * step
                            play( games, agente, agente2, 3, fileName )
                            
                            agente2.eps = 0
                            agente.eps = 0
                            play( 100, agente, agente2, 3, fileName )
                            with open(fileName, 'a', encoding='utf-8') as file:
                                file.write(",\n")
                            
    elif type == "MN" and type2 != "MN":
        for k in range( 1, 10 ):
            agente.depth = k
            print(f"k = {k}")
            for l in range( int( 1/step + 1 ) ):
                agente2.alpha = l * step
                for m in range( int( 1/step + 1 ) ):
                    agente2.gamma = m * step
                    for n in range( int( 1/step + 1 ) ):
                        agente2.eps = n * step
                        play( games, agente, agente2, 3, fileName )

                        agente2.eps = 0
                        play( 100, agente, agente2, 3, fileName )
                        with open(fileName, 'a', encoding='utf-8') as file:
                            file.write(",\n")
    
    elif type != "MN" and type2 == "MN":
        agente.alpha = i * step
        for j in range( int( 1/step + 1 ) ):
            agente.gamma = j * step
            print(f"j2 = {j}")
            for k in range( int( 1/step + 1 ) ):
                agente.eps = k * step
                for l in range( 1, 10 ):
                    agente2.depth = l
                    play( games, agente, agente2, 3, fileName )

                    agente.eps = 0
                    play( 100, agente, agente2, 3, fileName )
                    with open(fileName, 'a', encoding='utf-8') as file:
                        file.write(",\n")
    else:
        for k in range( 1, 10 ):
            agente.depth = k
            print(f"k2 = {k}")
            for l in range( 1, 10 ):
                agente2.depth = l
                play( games, agente, agente2, 3, fileName )
                with open(fileName, 'a', encoding='utf-8') as file:
                    file.write(",\n")
    
    print(f"Finalizado {type} contra {type2} i = {i}!")

def play( games : int, agente, agente2,  human, fileName ):
    a1 = 0
    a2 = 0
    d = 0

    for _ in range(games):
        game = Game( agente, agente2)
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
    
    with open(fileName, 'a', encoding='utf-8') as file:

        if type(agente).__name__ == "Minimax":
            begin = f'"{agente.depth}"'
        else:
            alpha1 = f'{agente.alpha:.2f}'.replace(".",",")
            gamma1 = f'{agente.gamma:.2f}'.replace(".",",")
            eps1 = f'{agente.eps:.2f}'.replace(".",",")
            begin = f'"{alpha1}","{gamma1}","{eps1}"'

        if type(agente2).__name__ == "Minimax":
            middle = f'"{agente2.depth}"'
        else:
            alpha2 = f'{agente2.alpha:.2f}'.replace(".",",")
            gamma2 = f'{agente2.gamma:.2f}'.replace(".",",")
            eps2 = f'{agente2.eps:.2f}'.replace(".",",")
            middle = f'"{alpha2}","{gamma2}","{eps2}"'

        file.write( f'{begin},{middle},{games},{a1},{a2},{d}\n')
    
def CompareSame( games, type, step =0.1 ):
    start_time = time.time()
    processes = []
    end = 11 
    if type == "MN":
        end = 10
    for i in range( 1, end ):
        fileName = f"C:/Users/Fernando Franco/Desktop/Comparações{type}{i}.csv"
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(f"Agente 1, {type}, Agente 2, {type}\n")
            begin = "Alpha 1, Gamma 1, Epsilon 1, "
            middle = "Alpha 2, Gamma 2, Epsilon 2, "
            extra = f"Jogos supondo sempre melhor jogada após treinamento,\n"
            if type == "MN":
                begin = "Profundidade, "
                middle = "Profundidade, "
                extra = ",\n"

            file.write(f"{begin}{middle}Partidas,Partidas Vencidas por 1,Partidas Vencidas por 2,Empates\n")
            file.write(extra)
        p = multiprocessing.Process(target=compSame, args=(i, type, fileName, step, games,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
    
    print("--- %s seconds ---" % (time.time() - start_time))
def compSame( i, type, fileName, step, games ):
    if type == "TD":
        agente = TD( 0, 0, 0 )
    elif type == "Q":
        agente = Q( 0, 0, 0 )
    elif type == "MN":
        agente = Minimax( i )

    print(f"Começando {type} i = {i}...")


    if type == "MN":
        play( games, agente, agente, 3, fileName )
    else:
        agente.alpha = i * step
        for j in range( int( 1/step + 1 ) ):
            agente.gamma = j * step
            #print(f"j = {j}")
            for k in range( int( 1/step + 1 ) ):
                agente.eps = k * step
                play( games, agente, agente, 3, fileName )
                agente.eps = 0
                play( 100, agente, agente, 3, fileName )
                with open(fileName, 'a', encoding='utf-8') as file:
                    file.write(",\n")

    print(f"Finalizado {type} i = {i}!")

def CompareAgainst( games, type, type2, step = 0.1 ):
    start_time = time.time()
    processes = []
    types = ["TD", "Q", "MN"]
    types2 = ["TD", "Q", "MN"]

    if type != "all":
        types = [type]
    if type2 != "all":
        types2 = [type2]
        
    for t in types:
        for t2 in types2:
            end = 11 
            if t == "MN":
                end = 2
            for i in range( 1, end ):
                p = multiprocessing.Process(target=compAgainst, args=(i, t, t2, fileName, step, games,))
                processes.append(p)
                p.start()

    for process in processes:
        process.join()
    
    print("--- %s seconds ---" % (time.time() - start_time))

def compAgainst( i, type, type2, fileName, step, games ):
    pass

def playAgainst( games, agente, agente2 ):
    a1 = 0
    a2 = 0
    d = 0

    for i in range(games):
        game = Game( agente, agente2)
        if i % 50 == 0:
            print(f"Partida {i}")
        result,player = game.training( 3 )
        if result == 100 or result == 400:
            d += 1
        elif result == 1000 and player == 1:
            a1 += 1
        else:
            a2 += 1
    
    print()

    if type(agente).__name__ == "Minimax":
        begin = f"Profundidade : {agente.depth} "
    else:
        begin = f"Alpha : {agente.alpha}, Gamma : {agente.gamma}, Epsilon : {agente.eps} "

    if type(agente2).__name__ == "Minimax":
        middle = f"Profundidade : {agente2.depth} "
    else:
        middle = f"Alpha : {agente2.alpha}, Gamma : {agente2.gamma}, Epsilon : {agente2.eps} "

    print(f"{begin}  {middle}Partidas : {games}, Partidas Vencidas por 1 : {a1}, Partidas Vencidas por 2 : {a2}, Empates : {d}\n")
    
if __name__ == '__main__': 
    # ---Usam todos os cores do pc cuidado para não crashar---
    #Compare(10)
    #CompareSame(50000, "Q")
    #CompareSame(50000, "MN")
    #CompareSame(50000, "TD")
    # ---------------------------------------------------------

    # alpha = 0.1, gamma = 1, eps = 1
    #
    agente = Minimax( 6 )
    agente2 = Q( 0.1, 1 , 1 )
    agente3 = TD( 0.1, 1 , 1 )
    playAgainst( 10000, agente, agente2)
    playAgainst( 10000, agente, agente3)

    agente2.eps = 0
    agente3.eps = 0
    playAgainst( 1000, agente2, agente3)
    playAgainst( 1000, agente3, agente2)

    # with open(f"TD {agente.alpha} {agente.gamma} 1", "wb") as output_file:
    #     pickle.dump(agente.Q, output_file)

