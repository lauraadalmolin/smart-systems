from genetic2022 import *

def run_bruteforce(itens, peso_max):
    n_itens = len(itens)
    
    # indivíduo inicial (todos zeros)
    individuo = BitArray(n_itens)
    
    # indivíduo final (todos uns)
    end = BitArray(n_itens)
    end.invert()
    
    # contador de combinações
    combos = 0

    # verifica todos possíveis indivíduos
    best = (0, individuo)
    
    while individuo.uint < end.uint:
        individuo = BitArray(uint = individuo.uint+1, length=n_itens)
        fit = fitness(individuo ,itens ,peso_max)

        if fit > best [0]:
            best = (fit, individuo)
        combos += 1

    print("Número de combinações (Brute Force): "+str(combos))
    
    return(best)
