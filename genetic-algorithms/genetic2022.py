from random import randint , random , getrandbits
from operator import add
from functools import reduce
from bitstring import BitArray

# cria um membro da população
# como um array de bits aleatórios
def individual(length, rand=True):
    if rand:
        return BitArray(uint=getrandbits(length), length=length)
    else:
        return BitArray(length)

# cria a população
def population(population_size, number_of_pictures):
    return [ individual(number_of_pictures) for _ in range(population_size) ]

# o fitness será a soma dos likes das fotos selecionadas
# caso o número de tags ultrapassar o número máximo permitido
# o fitness será zero
def fitness(individual, pictures, max_tags):
    # valores iniciais
    tags = 0
    likes = 0

    # para cada bit
    for (i, x) in enumerate(individual):
        # se estiver contido na mochila
        if x:
            tags += pictures[i][0]
            likes += pictures[i][1]

            # se exceder max_tags retorna zero
            if tags > max_tags:
                return 0.01 
            
    return likes

def tags(individual, pictures):
    tags = 0
    for (i, x) in enumerate(individual):
        if x:
            tags += pictures[i][0]
            
    return tags

# média de fitness da população
def media_fitness(population, pictures, max_tags):
    fitness_sum = reduce(add, (fitness(individual, pictures, max_tags) for individual in population))
    tags_sum = 10*reduce(add, (tags(individual, pictures) for individual in population))
    
    population_size = len(population) * 1.0
    
    avg_fitness = fitness_sum / population_size
    avg_tag_sum = tags_sum / population_size
    
    return (avg_fitness, avg_tag_sum)

# melhor fitness da população
def best_fitness(population, pictures, max_tags):
    graded = [(x, fitness(x, pictures, max_tags)) for x in population]
    best = max(graded, key=lambda graded:graded[1])

    return (best[1], 10*tags(best[0], pictures))

def generate_children(parents, number_of_parents, target_population_length):
    children = []
    
    while len(children) < target_population_length:
        # escolhe pai e mae no conjunto de pais
        male = randint(0, number_of_parents - 1)
        female = randint(0, number_of_parents - 1)
        
        if male != female:
            male = parents[male]
            female = parents[female]
            half = randint(2, len(male))
            
            # gera filho metade de cada
            child = male[:half] + female[half:]
            
            # adiciona novo filho a lista de filhos
            children.append(child)
    
    return children
            
def evolve(population, pictures, max_tags, elitism=5, r_parents=0.4, mutate=0.01):
    # gera tuplas de indivíduo e seu respectivo fitness
    graded = [(fitness(x, pictures, max_tags), x) for x in population]

    # ordena a população inicial por fitness
    graded = sorted(graded, key=lambda graded: graded[0], reverse=True)

    # número de pais necessários inicialmente
    # para que possa ser iniciada a reprodução posteriormente
    number_of_parents = int(len(graded)*r_parents)

    # no começo, a nova população está vazia
    new_population = []
    
    if elitism != 0:
        # os melhores já fazem parte da nova população
        new_population = [x[1] for x in graded][0:elitism]
        
    # faz a soma do fit total da população inicial
    fitness_aggregate = reduce(add, (x[0] for x in graded))
    
    # enquanto o número de indivíduos da nova população
    # for menor que o número de pais mínimo para que a reprodução aconteça
    # vamos gerar novos pais pelo método da roleta
    while len(new_population) < number_of_parents:
        pick = random()
        acum_fit = 0
        for _, (fit, individual) in enumerate(graded):
            acum_fit += fit/fitness_aggregate # distribuição acumulativa normalizada
            
            if acum_fit > pick:
                # adiciona novo pai na nova população
                new_population.append(individual)
                break
            
    # nesse ponto temos na nossa nova população todos os pais necessários
    # precisamos, então descobrir quantos filhos ainda precisam ser gerados
    
    # descobre quantos filhos terão que ser gerados além da elite e aleatórios
    target_population_length = len(population) - number_of_parents
    
    # começa a gerar os filhos que faltam
    children = generate_children(parents=new_population, number_of_parents=number_of_parents, target_population_length=target_population_length)

    # adiciona lista de filhos na população
    new_population.extend(children)
    
    # muta alguns indivíduos
    for i, individual in enumerate(new_population):
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            individual.invert(pos_to_mutate)
            
    return new_population
