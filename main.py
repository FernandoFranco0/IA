from game2 import Game
from q2 import Q2
from td import TD
import multiprocessing 

def Compare( type = "all", type2 = "all", step = 0.1):

    types = ["TD", "Q2"]
    types2 = ["TD", "Q2"]

    if type != "all":
        types = [type]
    if type2 != "all":
        types2 = [type2]

    processes = []
    for t in types:
        for t2 in types2:
            for i in range( 11 ):
                fileName = f"Comparações{t}{t2}{i}.csv"
                with open(fileName, 'w', encoding='utf-8') as file:
                    file.write(f"Agente 1, {t}, Agente 2, {t2}\n")
                    file.write("Alpha 1, Gamma 1, Epsilon 1, Alpha 2, Gamma 2, Epsilon 2, Partidas,Partidas Vencidas por 1,Partidas Vencidas por 2,Empates\n")
                p = multiprocessing.Process(target=compMp, args=(i, t, t2, fileName, step,))
                processes.append(p)
                p.start()
    
    for process in processes:
        process.join()


def compMp( i, type, type2, fileName, step ):

    if type == "TD":
        agente = TD( 0, 0, 0 )
    elif type == "Q2":
        agente = Q2( 0, 0, 0 )

    if type2 == "TD":
        agente2 = TD( 0, 0, 0 )
    elif type2 == "Q2": 
        agente2 = Q2( 0, 0, 0 )

    print(f"Começando {type} contra {type2} i = {i}...")

    agente.alpha = i * step
    for j in range( 11 ):
        agente.gamma = j * step
        print(f"j = {j}")
        for k in range( 11 ):
            agente.eps = k * step
            for l in range( 11 ):
                agente2.alpha = l * step
                for m in range( 11 ):
                    agente2.gamma = m * step
                    for n in range( 11 ):
                        agente2.eps = n * step
                        play( 50000, agente, agente2, 3, fileName )
    
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

        alpha1 = f'{agente.alpha:.2f}'.replace(".",",")
        gamma1 = f'{agente.gamma:.2f}'.replace(".",",")
        eps1 = f'{agente.eps:.2f}'.replace(".",",")

        alpha2 = f'{agente2.alpha:.2f}'.replace(".",",")
        gamma2 = f'{agente2.gamma:.2f}'.replace(".",",")
        eps2 = f'{agente2.eps:.2f}'.replace(".",",")

        file.write( f'"{alpha1}","{gamma1}","{eps1}","{alpha2}","{gamma2}","{eps2}",{games},{a1},{a2},{d}\n')
    
if __name__ == '__main__':
    Compare()