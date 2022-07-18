from matplotlib import pyplot as plt
from genetic2022 import *
from bruteforce import *
import time

# --- Definição das constantes ---

# imagens possíveis (número de tags, número de likes)
pictures = [(0, 60), (2, 80), (1, 200), (1, 10), (300, 20), (0, 155), (1, 65), (3, 270), (0, 95), (0, 28), (1, 39), (0, 86), (2, 8), (3, 84), (0, 92), (0, 73), (1, 20), (1, 14), (0, 20), (5, 180), (2, 130), (1, 350), (1, 370), (0, 780), (4, 550)]

# número de pictures
number_of_pictures = len(pictures)

# número máximo de tags
max_tags = 15

# --- Algoritmo de força bruta ---

print("--- Algoritmo de força bruta ---")
print("Número de imagens: " + str(number_of_pictures))

t0 = time.time()
bf_fit, bf_individual = run_bruteforce(pictures, max_tags)
t1 = time.time()

print("Melhor indivíduo: " + str(bf_individual))
print("Likes: " + str(bf_fit))

print("Tempo: " + str(t1-t0))

# --- Algoritmo genético ---

print("--- Algoritmo genético ---")

t0 = time.time()

# tamanho da população
population_size = 150

# criando a população
p = population(population_size, number_of_pictures)

# número de gerações para testar
epochs = 5000

# salva fitness para referência
media = media_fitness(p, pictures, max_tags)
best_f = best_fitness(p, pictures, max_tags)

# med fitness|med tags|best fitness|bets tags
fitness_history = [[media[0]],[media[1]],[best_f[0]],[best_f[1]]] 

for i in range(epochs):
    p = evolve(p, pictures , max_tags)
    media = media_fitness(p, pictures, max_tags)
    best_f = best_fitness(p, pictures, max_tags)
    fitness_history[0].append(media[0])
    fitness_history[1].append(media[1])
    fitness_history[2].append(best_f[0])
    fitness_history[3].append(best_f[1])

t1 = time.time()

print("Tempo: " + str(t1-t0))

best_individual = str(sorted(p, key=lambda p: p[0])[-1])
most_likes = str(fitness_history[2][-1])

print("Melhor indivíduo: " + best_individual)
print("Likes: " + most_likes)

# plotando os resultados

fig = plt.figure()
ax = plt.axes()

ax.plot(fitness_history[0])
ax.plot(fitness_history[2])
ax.plot(3404)
ax.plot(fitness_history[1])
ax.plot(fitness_history[3])

ax.legend(["Fitness Média", "Melhor Fitness", "Fitness Força Bruta", " Tags Médio (x10)", "Tags do Melhor (x10)"])

ax.grid(True)
plt.show()
